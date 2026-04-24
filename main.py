import os
import random
import anthropic
import requests
from datetime import datetime

ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]
LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
LINE_USER_ID = "Ubd780df324687bfa9caf63f29fbc431a"

THEMES = [
    "成長與蛻變", "放下與釋懷", "勇氣與行動", "活在當下", "自我接納",
    "人際關係", "創造力與靈感", "休息與充電", "好奇心與探索", "感恩與珍惜"
]

STYLES = [
    "帶點幽默和俏皮", "溫柔而堅定", "簡短有力像一句話的魔法"
    , "帶點哲學感但不說教"
]

def generate_affirmation(client: anthropic.Anthropic) -> str:
    today = datetime.now().strftime("%Y-%m-%d")
    theme = random.choice(THEMES)
    style = random.choice(STYLES)
    
    system_prompt = f"""你是一位開放、溫暖、務實、充滿正能量的生活導師。
你的任務是每天生成一段三語每日 affirmation，格式如下：

【Get ready to SLAY the day💅🏻✨】

🌸 中文
（一段溫暖有力的中文正向宣言，1-2句）

🌿 English
（A warm and empowering affirmation in English, 1-2 sentences）

🌻 Français
（Une affirmation chaleureuse et positive en français, 1-2 phrases）

今天的主題：{theme}
今天的語氣風格：{style}
不要使用陳腔濫調，也不要濫情，每天都要有新鮮感。"""

    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        system=system_prompt,
        messages=[
            {
                "role": "user",
                "content": f"請為今天（{today}）生成一段充滿正能量的三語每日 affirmation。",
            }
        ],
    )
    return next(block.text for block in response.content if block.type == "text")

def send_line_push(message: str) -> None:
    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}",
    }
    payload = {
        "to": LINE_USER_ID,
        "messages": [{"type": "text", "text": message}],
    }
    resp = requests.post(url, headers=headers, json=payload, timeout=10)
    if not resp.ok:
        raise Exception(f"LINE error {resp.status_code}: {resp.text}")
    print(f"LINE push sent successfully (status {resp.status_code})")

def main() -> None:
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    print("Generating affirmation...")
    affirmation = generate_affirmation(client)
    print(f"Generated:\n{affirmation}\n")
    send_line_push(affirmation)

if __name__ == "__main__":
    main()
