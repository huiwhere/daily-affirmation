import os
import anthropic
import requests
from datetime import datetime

ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]
LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
LINE_USER_ID = "Ubd780df324687bfa9caf63f29fbc431a"

SYSTEM_PROMPT = """你是一位溫暖、充滿正能量的生活導師。
你的任務是每天生成一段三語每日 affirmation（正向宣言），格式如下：

【今日宣言 · Daily Affirmation · Affirmation du Jour】

🌸 中文
（一段溫暖有力的中文正向宣言，2-3句）

🌿 English
（A warm and empowering affirmation in English, 2-3 sentences）

🌻 Français
（Une affirmation chaleureuse et positive en français, 2-3 phrases）

語氣要真誠、溫暖、充滿力量，像一位好朋友在鼓勵你。
不要使用陳腔濫調，每天都要有新鮮感。"""


def generate_affirmation(client: anthropic.Anthropic) -> str:
    today = datetime.now().strftime("%Y-%m-%d")
    response = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
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
    print(f"LINE response: {resp.status_code} {resp.text}")
    resp.raise_for_status()
    print(f"LINE push sent successfully (status {resp.status_code})")


def main() -> None:
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    print("Generating affirmation...")
    affirmation = generate_affirmation(client)
    print(f"Generated:\n{affirmation}\n")
    send_line_push(affirmation)


if __name__ == "__main__":
    main()
