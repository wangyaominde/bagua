from flask import Flask, render_template, request, jsonify, Response, stream_with_context
from ai_client import call_openai
import os
import json
import logging
import asyncio
from concurrent.futures import ThreadPoolExecutor
import time
import queue
import threading

app = Flask(__name__)
executor = ThreadPoolExecutor(max_workers=3)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 加载配置文件
def load_config():
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"加载配置文件失败：{str(e)}")
        return None

config = load_config()

# 加载城市数据
with open('city.json', 'r', encoding='utf-8') as f:
    city_data = json.load(f)

# 获取所有省份
provinces = list(set(city['province'] for cities in city_data.values() for city in cities))
provinces.sort()  # 按字母顺序排序

@app.route('/')
def index():
    return render_template('index.html', provinces=provinces)

@app.route('/get_cities/<province>')
def get_cities(province):
    cities = []
    for cities_list in city_data.values():
        for city in cities_list:
            if city['province'] == province:
                cities.append(city['name'])
    return jsonify(cities)

def generate_fortune_text():
    """生成一些占卜相关的文字，在等待AI响应时显示"""
    texts = [
        "正在摇卦...",
        "解读天机...",
        "推算命盘...",
        "分析八字...",
        "演算五行...",
        "推演命理...",
        "解读卦象...",
    ]
    for text in texts:
        yield f"data: {json.dumps({'type': 'status', 'content': text})}\n\n"
        time.sleep(0.5)

def stream_ai_response(user_input):
    """流式返回AI响应"""
    try:
        # 首先发送状态信息
        for status_data in generate_fortune_text():
            yield status_data

        # 调用AI接口
        logger.info("开始调用AI接口")
        system_prompt = config['system_prompt']['fortune_telling']
        
        user_message = f"""请为以下用户进行命理分析（信息格式：姓名 性别 出生年月日时（默认用户输入的是农历） 出生地）：
{user_input}

请提供详细的命理分析和人生建议。"""

        logger.info(f"系统提示词: {system_prompt}")
        logger.info(f"用户消息: {user_message}")
        
        # 使用流式API
        for chunk in call_openai(
            api_key=config['ai']['api_key'],
            base_url=config['ai']['base_url'],
            model=config['ai']['model'],
            temperature=config['ai']['temperature'],
            system_prompt=system_prompt,
            user_message=user_message,
            stream=True
        ):
            yield f"data: {json.dumps({'type': 'content', 'content': chunk})}\n\n"
        
        # 发送完成信号
        yield f"data: {json.dumps({'type': 'done'})}\n\n"
        
        logger.info("AI响应完成")
        
    except Exception as e:
        error_msg = f"很抱歉，系统出现错误：{str(e)}"
        logger.error(error_msg)
        yield f"data: {json.dumps({'type': 'error', 'content': error_msg})}\n\n"

@app.route('/calculate', methods=['POST'])
def calculate():
    user_input = request.form.get('user_input', '')
    if not user_input:
        return jsonify({"success": False, "error": "请输入信息"})
    
    return Response(
        stream_with_context(stream_ai_response(user_input)),
        mimetype='text/event-stream'
    )

if __name__ == '__main__':
    if not config:
        logger.error("错误：无法加载配置文件，请确保 config.json 文件存在且格式正确")
    else:
        logger.info("服务启动成功")
        app.run(host='0.0.0.0', port=9999, debug=True) 