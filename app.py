from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html lang="fa">
<head>
<meta charset="UTF-8">
<title>🍽️ ربات سفارش‌گیر رستوران</title>
<style>
body {
    font-family: 'Tahoma', sans-serif;
    background-color: #f0f2f5;
    direction: rtl;
    text-align: center;
    padding: 30px;
}
.header {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 10px;
    margin-bottom: 20px;
}
.header img {
    width: 50px;
    height: 50px;
}
h2 {
    color: #333;
    margin: 0;
}
.chat-container {
    width: 100%;
    max-width: 500px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    height: 550px;
    border-radius: 15px;
    background: #fff;
    box-shadow: 0 6px 18px rgba(0,0,0,0.2);
    overflow: hidden;
}
.chat-box {
    flex: 1;
    padding: 15px;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
}
.input-container {
    display: flex;
    border-top: 1px solid #ccc;
}
input {
    flex: 1;
    padding: 14px;
    border: none;
    outline: none;
    font-size: 14px;
    border-radius: 0;
}
button {
    padding: 14px 20px;
    border: none;
    background-color: #28a745;
    color: white;
    cursor: pointer;
    transition: background 0.3s, transform 0.2s;
    font-weight: bold;
}
button:hover {
    background-color: #218838;
    transform: scale(1.05);
}
.message {
    display: flex;
    align-items: center;
    gap: 8px;
    margin: 8px 0;
    padding: 12px 16px;
    border-radius: 25px;
    max-width: 75%;
    word-wrap: break-word;
    font-size: 14px;
    clear: both;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    transition: background 0.3s;
}
.user-msg {
    background-color: #d1e7dd;
    align-self: flex-start;
    float: left;
    justify-content: flex-start;
}
.bot-msg {
    background-color: #e2e3e5;
    align-self: flex-end;
    float: right;
    justify-content: flex-end;
}
.menu-item {
    background-color: #fff3cd;
    padding: 10px 14px;
    margin: 6px 0;
    border-radius: 15px;
    text-align: right;
    box-shadow: 0 2px 8px rgba(0,0,0,0.15);
    cursor: pointer;
    transition: background 0.3s, transform 0.2s;
    font-weight: bold;
}
.menu-item:hover {
    background-color: #ffeeba;
    transform: scale(1.02);
}
.icon {
    width: 24px;
    height: 24px;
    flex-shrink: 0;
}
</style>
</head>
<body>

<div class="header">
    <img src="https://cdn-icons-png.flaticon.com/512/1046/1046784.png" alt="Restaurant Icon">
    <h2>ربات سفارش‌گیر رستوران</h2>
</div>

<div class="chat-container">
    <div class="chat-box" id="chat"></div>
    <div class="input-container">
        <input type="text" id="question" placeholder="سوال خود را بنویسید...">
        <button onclick="sendQuestion()">ارسال</button>
    </div>
</div>

<script>
const chatBox = document.getElementById("chat");

// مسیر تصاویر آیکون
const userIcon = "https://cdn-icons-png.flaticon.com/512/3135/3135715.png";
const botIcon = "https://cdn-icons-png.flaticon.com/512/6134/6134346.png";

const menu = [
    {name: "🍕 پیتزا", desc: "پیتزا شامل پپرونی، سبزیجات، مخصوص در اندازه کوچک، متوسط و بزرگ."},
    {name: "🍔 برگر", desc: "برگر کلاسیک، چیزبرگر و دوبل با نان تازه و گوشت خوشمزه."},
    {name: "🍝 پاستا", desc: "پاستا آلفردو و بولونز با سس مخصوص رستوران."},
    {name: "🥗 سالاد", desc: "سالاد تازه با سبزیجات متنوع و سس مخصوص."},
    {name: "🥤 نوشیدنی‌ها", desc: "انواع نوشابه، آبمیوه و شیک‌های خوشمزه."}
];

function showMenu() {
    addMessage("📋 منوی ما:", "bot-msg");
    menu.forEach(item => {
        const div = document.createElement("div");
        div.className = "menu-item bot-msg";
        div.textContent = item.name;
        div.onclick = () => sendMenuSelection(item.name);
        chatBox.appendChild(div);
    });
    chatBox.scrollTop = chatBox.scrollHeight;
}

function sendMenuSelection(text) {
    addMessage(text, "user-msg");
    fetch("/ask", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({question: text})
    })
    .then(res => res.json())
    .then(data => addMessage(data.answer, "bot-msg"))
    .catch(err => addMessage("⚠️ خطا: " + err.message, "bot-msg"));
    chatBox.scrollTop = chatBox.scrollHeight;
}

async function sendQuestion() {
    const q = document.getElementById("question").value.trim();
    if (!q) return;
    addMessage(q, "user-msg");
    document.getElementById("question").value = "";

    try {
        const res = await fetch("/ask", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({question: q})
        });

        if (!res.ok) throw new Error("خطا در دریافت پاسخ");

        const data = await res.json();
        if(data.answer === "SHOW_MENU"){
            showMenu();
        } else {
            addMessage(data.answer, "bot-msg");
        }
    } catch (err) {
        addMessage("⚠️ خطا: " + err.message, "bot-msg");
    }
}

function addMessage(text, cls) {
    const msg = document.createElement("div");
    msg.className = "message " + cls;

    const iconImg = document.createElement("img");
    iconImg.src = cls === "user-msg" ? userIcon : botIcon;
    iconImg.className = "icon";

    const content = document.createElement("span");
    content.textContent = text;

    if(cls === "user-msg"){
        msg.appendChild(iconImg);
        msg.appendChild(content);
    } else {
        msg.appendChild(content);
        msg.appendChild(iconImg);
    }

    chatBox.appendChild(msg);
    chatBox.scrollTop = chatBox.scrollHeight;
}
</script>

</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_PAGE)

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data.get("question", "").lower()

    if "سلام" in question or "خوش آمد" in question:
        answer = "سلام! خوش اومدی 😊 می‌خوای منو رو ببینی یا سفارش بدی؟"
    elif "ساعت کاری" in question or "زمان باز" in question:
        answer = "ما هر روز از ۱۲ ظهر تا ۱۲ شب باز هستیم."
    elif "منو" in question or "غذا" in question:
        answer = "SHOW_MENU"
    elif "آدرس" in question or "کجاست" in question:
        answer = "ما در خیابان انقلاب، پلاک ۲۲ قرار داریم."
    elif "سفارش" in question or "چطور سفارش بدم" in question:
        answer = "می‌تونی از همین ربات سفارش بدی یا با شماره ما تماس بگیری. می‌خوای ثبت کنم برات؟"
    elif "🍕 پیتزا" in question or "پیتزا" in question:
        answer = "پیتزا شامل پپرونی، سبزیجات، مخصوص در اندازه کوچک، متوسط و بزرگ."
    elif "🍔 برگر" in question or "برگر" in question:
        answer = "برگر کلاسیک، چیزبرگر و دوبل با نان تازه و گوشت خوشمزه."
    elif "🍝 پاستا" in question or "پاستا" in question:
        answer = "پاستا آلفردو و بولونز با سس مخصوص رستوران."
    elif "🥗 سالاد" in question or "سالاد" in question:
        answer = "سالاد تازه با سبزیجات متنوع و سس مخصوص."
    elif "🥤 نوشیدنی" in question or "نوشیدنی‌ها" in question:
        answer = "انواع نوشابه، آبمیوه و شیک‌های خوشمزه."
    else:
        answer = "متوجه نشدم 😅 لطفاً کمی واضح‌تر بپرس یا از منو کمک بگیر."

    return jsonify({"answer": answer})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


