import os, sys, json, subprocess, requests, tempfile, base64, time
from datetime import datetime
from openai import OpenAI

OPENAI_KEY = os.getenv("OPENAI_KEY")

def generate_idea():
    client = OpenAI(api_key=OPENAI_KEY)
    prompt = ("Propose une idée d'extrait voyage 15 sec, "
              "donne titre, description 250 car, hashtags, "
              "et voice-over 35 mots.")
    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}],
        temperature=1.2
    )
    idea = json.loads(res.choices[0].message.content)
    with open("idea.json","w") as f: json.dump(idea,f)
    print("Idea saved")

def gen_video():
    idea = json.load(open("idea.json"))
    # --- Appel Runway Gen-2 (simplifié) ---
    headers = {"Authorization": f"Bearer {os.getenv('RUNWAY_KEY')}",
               "Content-Type": "application/json"}
    data = {"prompt": idea["runway_prompt"], "duration": 15}
    job = requests.post("https://api.runwayml.com/v1/generate/video", json=data, headers=headers).json()
    # Ici on devrait attendre le job… pour le test on créera un clip noir
    subprocess.run(["ffmpeg","-f","lavfi","-i","color=black:s=1080x1920:d=15","clip.mp4","-y"])
    print("Video ready")

def merge():
    idea = json.load(open("idea.json"))
    # --- Voice over ElevenLabs ---
    voice = requests.post(
        "https://api.elevenlabs.io/v1/text-to-speech/LeFrenchWarm/stream",
        headers={"xi-api-key": os.getenv("ELEVEN_KEY")},
        json={"text": idea["voiceover"], "model_id":"eleven_multilingual_v2"})
    open("voice.mp3","wb").write(voice.content)
    subprocess.run([
        "ffmpeg","-i","clip.mp4","-i","voice.mp3",
        "-c:v","copy","-c:a","aac","output.mp4","-y"])
    print("Merged audio/video")

def upload():
    idea = json.load(open("idea.json"))
    token = os.getenv("TIKTOK_TOKEN")   # token long-durée obtenu via OAuth
    # 1. /video/upload/
    res1 = requests.post(
        "https://open.tiktokapis.com/v2/post/publish/video/upload/",
        headers={"Authorization":f"Bearer {token}"},
        params={"upload_type":"video"},
    )
    upload_url = res1.json()["data"]["upload_url"]
    vid = open("output.mp4","rb").read()
    requests.put(upload_url, data=vid, headers={"Content-Type":"video/mp4"})
    # 2. /video/publish/
    body = {
      "text": idea["description"],
      "video_id": res1.json()["data"]["video_id"],
      "draft": os.getenv("POST_MODE","draft")=="draft"
    }
    pub = requests.post(
        "https://open.tiktokapis.com/v2/post/publish/video/publish/",
        headers={"Authorization":f"Bearer {token}",
                 "Content-Type":"application/json"},
        json=body).json()
    print("Publish status:", pub)

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv)>1 else "idea"
    {"idea":generate_idea,
     "video":gen_video,
     "merge":merge,
     "upload":upload}[cmd]()
