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
h2 {
    color: #333;
    margin-bottom: 20px;
}
.chat-container {
    width: 100%;
    max-width: 500px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    height: 500px;
    border-radius: 12px;
    background: #fff;
    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
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
    padding: 12px;
    border: none;
    outline: none;
    font-size: 14px;
}
button {
    padding: 12px 18px;
    border: none;
    background-color: #28a745;
    color: white;
    cursor: pointer;
    transition: background 0.3s;
}
button:hover {
    background-color: #218838;
}
.message {
    margin: 6px 0;
    padding: 10px 14px;
    border-radius: 20px;
    max-width: 75%;
    word-wrap: break-word;
    font-size: 14px;
}
.user-msg {
    background-color: #d1e7dd;
    align-self: flex-start;
}
.bot-msg {
    background-color: #e2e3e5;
    align-self: flex-end;
}
</style>
</head>
<body>

<h2>🍔 ربات سفارش‌گیر رستوران</h2>

<div class="chat-container">
    <div class="chat-box" id="chat"></div>
    <div class="input-container">
        <input type="text" id="question" placeholder="سوال خود را بنویسید...">
        <button onclick="sendQuestion()">ارسال</button>
    </div>
</div>

<script>
const chatBox = document.getElementById("chat");

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
        addMessage(data.answer, "bot-msg");
    } catch (err) {
        addMessage("⚠️ خطا: " + err.message, "bot-msg");
    }
}

function addMessage(text, cls) {
    const msg = document.createElement("div");
    msg.className = "message " + cls;
    msg.textContent = text;
    chatBox.appendChild(msg);
    chatBox.scrollTop = chatBox.scrollHeight; // اسکرول خودکار به پایین
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

    # پاسخ‌های هوشمند و دسته‌بندی شده
    if "سلام" in question or "خوش آمد" in question:
        answer = "سلام! خوش اومدی 😊 می‌خوای منو رو ببینی یا سفارش بدی؟"
    elif "ساعت کاری" in question or "زمان باز" in question:
        answer = "ما هر روز از ۱۲ ظهر تا ۱۲ شب باز هستیم."
    elif "منو" in question or "غذا" in question:
        answer = ("منوی ما شامل:\n"
                  "🍕 پیتزا: پپرونی، سبزیجات، مخصوص\n"
                  "🍔 برگر: کلاسیک، چیزبرگر، دوبل\n"
                  "🍝 پاستا: آلفردو، بولونز\n"
                  "🥗 سالاد و نوشیدنی‌ها\n"
                  "می‌خوای عکس یکی از غذاها رو ببینی یا سفارش بدی؟")
    elif "آدرس" in question or "کجاست" in question:
        answer = "ما در خیابان انقلاب، پلاک ۲۲ قرار داریم."
    elif "سفارش" in question or "چطور سفارش بدم" in question:
        answer = "می‌تونی از همین ربات سفارش بدی یا با شماره ما تماس بگیری. می‌خوای ثبت کنم برات؟"
    else:
        answer = "متوجه نشدم 😅 لطفاً کمی واضح‌تر بپرس یا از منو کمک بگیر."

    return jsonify({"answer": answer})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
