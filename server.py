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
    <h1>Pico Cloud Remote Control</h1>
    <p><a href="/api/on"><button style="font-size:30px">LED ON</button></a></p>
    <p><a href="/api/off"><button style="font-size:30px">LED OFF</button></a></p>
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
