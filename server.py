from flask import Flask, jsonify

app = Flask(__name__)

PAGE = '''<!doctype html>
<html lang="zh-Hant">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Pico 2 W Cloud Server</title>
  <style>
    body { font-family: system-ui, sans-serif; max-width: 560px; margin: 48px auto; padding: 0 20px; }
    .card { border: 1px solid #ddd; border-radius: 16px; padding: 24px; }
    button { font-size: 18px; padding: 12px 18px; margin-right: 8px; }
    #status { margin-top: 18px; font-weight: 700; }
  </style>
</head>
<body>
  <div class="card">
    <h1>☁️ Pico 2 W Cloud Server</h1>
    <p>手機已經連上 Vercel Server。</p>
    <button onclick="ping()">測試 Server</button>
    <div id="status">尚未測試</div>
  </div>
  <script>
    async function ping() {
      const r = await fetch('/api/ping');
      const data = await r.json();
      document.getElementById('status').textContent = data.message;
    }
  </script>
</body>
</html>'''

@app.get("/")
def home():
    return PAGE

@app.get("/api/ping")
def ping():
    return jsonify(ok=True, message="手機 ↔ Vercel Server：連線成功！")
