import http.client
import json
from conf import API_KEY  # 假设API_KEY已移至conf.py

def build_video_script(keyword):
    content = f'请帮我生成一个视频脚本，内容是关于{keyword}的视频，我将用于使用可灵生成视频，只返回脚本内容不要返回其他的无关内容'
    conn = http.client.HTTPSConnection("api.gpt.ge")
    payload = json.dumps({
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": content}],
        "max_tokens": 1688,
        "temperature": 0.5,
        "stream": False
    })
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    conn.request("POST", "/v1/chat/completions", payload, headers)
    res = conn.getresponse()
    data = json.loads(res.read())
    conn.close()
    return data["choices"][0]["message"]["content"]

def build_video(script):
    conn = http.client.HTTPSConnection("api.gpt.ge")
    payload = json.dumps({
        "model_name": "kling-v1-6",
        "prompt": script,
        "mode": "std",
        "aspect_ratio": "1:1",
        "duration": "5"
    })
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    conn.request("POST", "/kling/v1/videos/text2video", payload, headers)
    res = conn.getresponse()
    return res.read().decode("utf-8")

def keling_query(task_id):
    url = f'/kling/v1/videos/text2video/{task_id}'
    conn = http.client.HTTPSConnection("api.gpt.ge")
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    conn.request("GET", url, '', headers)
    res = conn.getresponse()
    return res.read().decode("utf-8")