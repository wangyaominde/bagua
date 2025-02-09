# 八卦命理分析系统

这是一个基于人工智能的命理分析系统，可以为用户提供专业的八字分析和人生建议。

## 功能特点

- 支持农历生辰八字分析
- 智能命理推演
- 实时流式响应
- 覆盖全国地域信息
- 提供详细的命理分析报告，包括：
  - 八字信息解读
  - 事业发展建议
  - 财运分析
  - 健康建议
  - 人际关系分析

## 安装步骤

1. 克隆项目到本地：
```bash
git clone https://github.com/wangyaominde/bagua.git
cd [项目目录]
```

2. 创建并激活虚拟环境：
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
.\venv\Scripts\activate  # Windows
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

4. 配置系统：
- 复制 `config.json` 文件并填写必要的配置信息：
  - 设置 AI API 密钥
  - 配置 API 基础URL（默认使用 SiliconFlow API）
  - 根据需要调整其他参数

## 使用方法

1. 启动应用：
```bash
python app.py
```

2. 打开浏览器访问：`http://localhost:9999`

3. 在页面上输入以下信息：
   - 姓名
   - 性别
   - 出生年月日时（农历）
   - 选择出生地（省份和城市）

4. 点击分析按钮，系统将生成详细的命理分析报告

## 注意事项

- 确保输入的生日信息为农历日期
- 系统需要联网以访问 AI 服务
- 请确保 config.json 中的 API 密钥配置正确

## 技术栈

- Python
- Flask
- DeepSeek AI API
- JavaScript
- HTML/CSS

## 日志

系统日志默认保存在 `logs` 目录下，可通过配置文件调整日志级别。

## 配置说明

配置文件 `config.json` 包含以下主要设置：

- AI 服务配置（API密钥、模型选择等）
- 系统提示词配置
- 日志配置
