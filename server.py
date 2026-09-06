import os

import requests
from flask import Flask, jsonify

app = Flask(__name__)

UPSTASH_URL = os.environ["UPSTASH_KV_REST_API_URL"]
UPSTASH_TOKEN = os.environ["UPSTASH_KV_REST_API_TOKEN"]

headers = {
    "Authorization": f"Bearer {UPSTASH_TOKEN}",
    "Content-Type": "application/json",
}


def redis_command(command):
    response = requests.post(UPSTASH_URL, headers=headers, json=command, timeout=10)
    response.raise_for_status()
    return response.json()


@app.get("/")
def home():
    return """
    <!doctype html>
    <html lang="zh-Hant">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Pico WS2812 控制器</title>
    <style>
      * { box-sizing: border-box; }
      body { margin: 0; min-height: 100vh; display: grid; place-items: center;
             background: #10131a; color: #f5f7fb; font-family: system-ui, sans-serif; }
      main { width: min(92vw, 420px); padding: 28px 22px; text-align: center; }
      h1 { font-size: 1.7rem; margin: 0 0 24px; }
      button { width: 100%; min-height: 76px; margin: 8px 0; border: 0; border-radius: 16px;
               color: white; font-size: 1.35rem; font-weight: 700; }
      #on { background: #e53935; } #off { background: #374151; }
      #status { min-height: 1.5em; margin-top: 18px; color: #b9c2d0; }
    </style>
    <main>
      <h1>Pico WS2812 燈光控制</h1>
      <button id="on">開燈</button>
      <button id="off">關燈</button>
      <div id="status">尚未操作</div>
    </main>
    <script>
      const status = document.querySelector('#status');
      async function setLight(path, label) {
        status.textContent = '連線中…';
        try {
          const response = await fetch(path);
          if (!response.ok) throw new Error('HTTP ' + response.status);
          const data = await response.json();
          status.textContent = data.command + '（完成）';
        } catch (error) { status.textContent = '操作失敗：' + error.message; }
      }
      document.querySelector('#on').onclick = () => setLight('/api/on', '開燈');
      document.querySelector('#off').onclick = () => setLight('/api/off', '關燈');
    </script>
    </html>
    """


@app.get("/api/on")
def led_on():
    redis_command(["SET", "command", "LED_ON"])
    return jsonify(ok=True, command="LED_ON")


@app.get("/api/off")
def led_off():
    redis_command(["SET", "command", "LED_OFF"])
    return jsonify(ok=True, command="LED_OFF")


@app.get("/api/command")
def get_command():
    result = redis_command(["GET", "command"])
    return jsonify(command=result.get("result") or "LED_OFF")


@app.get("/api/ping")
def ping():
    return jsonify(ok=True, message="Pico ↔ Vercel Server：連線成功！")
