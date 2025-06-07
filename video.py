
import os
import requests
import json
import http.client
import json
import sqlite3
from conf import BASE_DIR
from pathlib import Path
# 配置API密钥
API_KEY = 'sk-nciFMuKSriJ0xEJEF29e2a93B13f41A2Ab90F9De9106D1F2'
API_HOST = 'api.gpt.ge'


def get_person_timeline(name):
    """调用AI检索人物重大活动轨迹"""
    prompt = f"生成{name}的详细生平时间线，按年份分段列出重大事件，只返回核心内容，其他无关的不要返回"
    conn = http.client.HTTPSConnection(API_HOST)
    payload = json.dumps({
        "model": "deepseek-chat",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": 1688,
        "temperature": 0.5,
        "stream": False
    })
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        'Content-Type': 'application/json'
    }
    conn.request("POST", "/v1/chat/completions", payload, headers)
    res = conn.getresponse()
    data = res.read()
    data = json.loads(data)
    conn.close()
    res =  data["choices"][0]["message"]["content"]
    return res

def optimize_prompt(person_name,text_segment):
    """优化视频提示词"""
    prompt = f"""请就 {person_name} {text_segment},扩展一段视频内容描述 只返回正文其他不要返回"""
    conn = http.client.HTTPSConnection(API_HOST)
    payload = json.dumps({
        "model": "deepseek-chat",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": 1688,
        "temperature": 0.5,
        "stream": False
    })
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        'Content-Type': 'application/json'
    }
    conn.request("POST", "/v1/chat/completions", payload, headers)
    res = conn.getresponse()
    data = res.read()
    data = json.loads(data)
    conn.close()
    res =  data["choices"][0]["message"]["content"]
    return res


def buildVideo(script):
    conn = http.client.HTTPSConnection("api.gpt.ge")
    payload = json.dumps({
        "model_name": "kling-v1-6",
        "prompt": script,
        "mode": "std",
        "aspect_ratio": "1:1",
        "duration": "5"
    })
    headers = {
    "Authorization": f"Bearer {API_KEY}",
    'Content-Type': 'application/json'
    }
    conn.request("POST", "/kling/v1/videos/text2video", payload, headers)
    res = conn.getresponse()
    data = res.read()
    data = json.loads(data)
    conn.close()
    task_id =  data["data"]['task_id']
    return task_id

def batchSaveTaskData(list):
    # 循环list  插入数据库
    with sqlite3.connect(Path(BASE_DIR / "db" / "database.db")) as conn:
        for item in list:
            cursor = conn.cursor()
            cursor.execute('''
                            INSERT INTO persion (persion,sort,title,script,task_id,status)
                            VALUES (?,?,?,?,?,?)
                            ''', (item['persion'],item['index'],item['title'],item['script'],item['task_id'],1))
        
            conn.commit()


def main():
    person_name = '辛弃疾'
    
    # 1. 获取人物时间线
    timeline = get_person_timeline(person_name)
    segments = timeline.split("\n\n")  # 假设按空行分段
    
    # 2. 处理每个时间段
    video_clips = []
    for i, segment in enumerate(segments[:]):  # 限制生成3段演示
        
        # 优化提示词
        optimized = optimize_prompt(person_name,segment)
        
        
        # 生成视频片段
        task_id = buildVideo(optimized)



        if i > 0:
            video_clips.append({
                'persion': person_name,
                'index': int(i+1),
                'title': segment,
                'script': optimized,
                'task_id': task_id
            })
    

    # 保存数据库
    batchSaveTaskData(video_clips)
    # 3. 合成最终视频
    # final_video = concatenate_videoclips(video_clips)
    # output_path = f"{person_name}_biography.mp4"
    # final_video.write_videofile(output_path, fps=24)
    # print(f"视频已生成: {output_path}")

if __name__ == "__main__":
    main()
