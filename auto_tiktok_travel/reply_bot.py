"""Reply bot — listens to comment webhook and responds using GPT."""

import os, json

def reply(comment_text):
    # TODO: generate short friendly answer via OpenAI
    return "Merci ! 😊"

if __name__ == "__main__":
    payload_path = os.environ.get("GITHUB_EVENT_PATH", "event.json")
    if os.path.exists(payload_path):
        data = json.load(open(payload_path))
        comment = data.get("comment", {}).get("text", "")
        response = reply(comment)
        print("Would reply:", response)