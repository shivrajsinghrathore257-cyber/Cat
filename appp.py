import os, json, uuid
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
DB_FILE = "messages_db.json"
UPLOAD_FOLDER = 'static/uploads'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# 🔥 AUTO REPLY WITH BETTER SPACING
AUTO_REPLY = """🚀 *COLOUR TRADING PROFIT MISSION* 💸

Sabka profit karane ke liye humne ek special channel banaya hai! 

📊 *KAISA KAAM KAREGA?*

1️⃣ Channel mein sirf 50 experts honge.
2️⃣ Har period ka ek POLL aayega.
3️⃣ Do options: MOTA (Big) aur PATLA (Small).
4️⃣ Jis option pe sabse zyada VOTES honge, wahi trade leni hai! 📈

⚠️ *LEVELS:* Isme hamesha 5 Level tak Fund Manage rakhna hai.

🎁 *FREE TRIAL:* ek session aapka FREE TRIAL hoga. Register karke screenshot bheje:
https://www.in999pp.com/#/register?invitationCode=32775781092

✅ *JOINING PROCESS:* ₹500 deposit karein aur screenshot yahan bhejein.

💎 *WEEKLY ACCESS:* ₹300 pay karke weekly access lein.

🙏 THANKS FOR READING!"""

def load_db():
    if not os.path.exists(DB_FILE): return {}
    with open(DB_FILE, "r") as f: return json.load(f)

def save_db(data):
    with open(DB_FILE, "w") as f: json.dump(data, f, indent=4)

@app.route('/')
def index(): return render_template('index.html')

@app.route('/admin_panel')
def admin(): return render_template('admin.html')

@app.route('/get_messages')
def get_messages(): return jsonify(load_db())

@app.route('/send', methods=['POST'])
def send():
    db = load_db()
    sender = request.form.get('sender')
    role = request.form.get('role', 'user')
    text = request.form.get('text', '')
    msg_type = 'text'

    if sender not in db:
        db[sender] = {"messages": [], "unread": False}

    if 'image' in request.files:
        file = request.files['image']
        filename = str(uuid.uuid4()) + ".jpg"
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        text = "/static/uploads/" + filename
        msg_type = 'image'

    if text:
        db[sender]["messages"].append({"text": text, "role": role, "type": msg_type})
        if role == 'user':
            db[sender]["unread"] = True
            if len([m for m in db[sender]["messages"] if m['role']=='user']) == 1:
                db[sender]["messages"].append({"text": AUTO_REPLY, "role": "admin", "type": "text"})
        else:
            db[sender]["unread"] = False
    save_db(db)
    return jsonify({"status": "success"})

@app.route('/mark_seen', methods=['POST'])
def mark_seen():
    db = load_db()
    user = request.json.get('user')
    if user in db:
        db[user]["unread"] = False
        save_db(db)
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
