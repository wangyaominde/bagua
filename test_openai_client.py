from openai_client import call_openai

def test_deepseek_api():
    """
    测试使用 DeepSeek API 的函数
    """
    # DeepSeek API 配置
    API_KEY = "sk-3577d6aa8af94c1780d8938d1c99c0fc"
    BASE_URL = "https://api.deepseek.com"
    MODEL = "deepseek-chat"
    
    # 测试用例1：基础对话
    print("\n=== 测试用例1：基础对话 ===")
    result1 = call_openai(
        api_key=API_KEY,
        base_url=BASE_URL,
        model=MODEL,
        user_message="你好，请用中文介绍一下你自己"
    )
    print("测试用例1结果:", result1)
    
    # 测试用例2：专业问题
    print("\n=== 测试用例2：专业问题 ===")
    result2 = call_openai(
        api_key=API_KEY,
        base_url=BASE_URL,
        model=MODEL,
        temperature=0.8,
        system_prompt="你是一个专业的人工智能专家",
        user_message="请简单解释一下什么是深度学习"
    )
    print("测试用例2结果:", result2)
    
    # 测试用例3：创意写作
    print("\n=== 测试用例3：创意写作 ===")
    result3 = call_openai(
        api_key=API_KEY,
        base_url=BASE_URL,
        model=MODEL,
        temperature=0.9,
        system_prompt="你是一个富有创造力的作家",
        user_message="请写一个简短的关于春天的诗"
    )
    print("测试用例3结果:", result3)

if __name__ == "__main__":
    print("开始测试 DeepSeek API...")
    test_deepseek_api()
    print("\n所有测试完成！") 