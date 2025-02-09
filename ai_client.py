import openai
from typing import Optional, Union, Generator

def call_openai_stream(
    api_key: str,
    model: str = "gpt-3.5-turbo",
    temperature: float = 0.7,
    base_url: Optional[str] = None,
    system_prompt: str = "You are a helpful assistant.",
    user_message: str = "Hello!"
) -> Generator[str, None, None]:
    """
    流式调用 OpenAI API 的函数
    
    Args:
        api_key (str): OpenAI API 密钥
        model (str): 使用的模型名称，默认为 gpt-3.5-turbo
        temperature (float): 温度参数，控制输出的随机性，默认为 0.7
        base_url (str, optional): 自定义的 API 基础 URL，默认为 None
        system_prompt (str): system 角色的提示词，默认为标准助手提示词
        user_message (str): 用户的输入消息
        
    Yields:
        str: AI 的响应内容片段
    """
    # 配置客户端
    client = openai.OpenAI(
        api_key=api_key,
        base_url=base_url
    )
    
    try:
        response = client.chat.completions.create(
            model=model,
            temperature=temperature,
            stream=True,  # 启用流式传输
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
        )
        
        for chunk in response:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
            
    except Exception as e:
        yield f"调用 API 时发生错误: {str(e)}"

def call_openai(
    api_key: str,
    model: str = "gpt-3.5-turbo",
    temperature: float = 0.7,
    base_url: Optional[str] = None,
    system_prompt: str = "You are a helpful assistant.",
    user_message: str = "Hello!",
    stream: bool = False
) -> Union[str, Generator[str, None, None]]:
    """
    调用 OpenAI API 的函数，支持流式和非流式两种模式
    
    Args:
        api_key (str): OpenAI API 密钥
        model (str): 使用的模型名称，默认为 gpt-3.5-turbo
        temperature (float): 温度参数，控制输出的随机性，默认为 0.7
        base_url (str, optional): 自定义的 API 基础 URL，默认为 None
        system_prompt (str): system 角色的提示词，默认为标准助手提示词
        user_message (str): 用户的输入消息
        stream (bool): 是否使用流式传输，默认为 False
        
    Returns:
        Union[str, Generator[str, None, None]]: 如果 stream=False 返回完整响应字符串，否则返回生成器
    """
    if stream:
        return call_openai_stream(
            api_key=api_key,
            model=model,
            temperature=temperature,
            base_url=base_url,
            system_prompt=system_prompt,
            user_message=user_message
        )
    
    # 配置客户端
    client = openai.OpenAI(
        api_key=api_key,
        base_url=base_url
    )
    
    try:
        response = client.chat.completions.create(
            model=model,
            temperature=temperature,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"调用 API 时发生错误: {str(e)}"

# 使用示例
if __name__ == "__main__":
    # 这里替换为你的 API 密钥
    API_KEY = "your-api-key-here"
    
    # 基础调用示例
    result = call_openai(
        api_key=API_KEY,
        user_message="你好，请介绍一下你自己"
    )
    print("基础调用结果:", result)
    
    # 自定义参数调用示例
    custom_result = call_openai(
        api_key=API_KEY,
        model="gpt-4",
        temperature=0.9,
        base_url="https://custom-api-url.com/v1",  # 可选的自定义 API URL
        system_prompt="你是一个专业的 Python 编程专家",
        user_message="请解释什么是装饰器"
    )
    print("自定义调用结果:", custom_result) 