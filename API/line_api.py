import requests

CHANNEL_TOKEN = "Bearer A826gnrm/xC5fRqoU4e68jq7QTUiFEs9hIgzgfBvn3EXllJvTwbs6guCg/zfhiLvDi/Ry" \
                "+22GepsEx8zYCh5LdCXOlDYHCWsJpm+1qJTCzQ+HSSMuyBhsuZNjhsUTKcEEBhE2MLXZlW2M+djdOat2gdB04t89/1O" \
                "/w1cDnyilFU= "


def broadcast(text: str) -> None:
    api_url = "https://api.line.me/v2/bot/message/broadcast"

    payload = {
        "messages": [
            {
                "type": "text",
                "text": text
            }
        ]
    }

    headers = {
        "Authorization": CHANNEL_TOKEN,
        "Content-Type": "application/json"
    }

    requests.post(api_url, headers=headers, json=payload)
