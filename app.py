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
  background-color: #f2f2f2;
  direction: rtl;
  text-align: center;
  padding: 30px;
}
h2 {
  color: #333;
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
}
.input-container {
  display: flex;
  border-top: 1px solid #ccc;
}
input {
  flex: 1;
  padding: 12px;
  border: none;
  border-radius: 0;
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
  margin: 8px 0;
  padding: 10px 14px;
  border-radius: 20px;
  display: inline-block;
  max-width: 80%;
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
  chatBox.scrollTop = chatBox.scrollHeight; // اسکرول خودکار
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

    if "ساعت کاری" in question:
        answer = "ساعت کاری ما از ۱۲ ظهر تا ۱۲ شب است."
    elif "منو" in question:
        answer = "منوی ما شامل پیتزا، برگر، پاستا و نوشیدنی است."
    elif "آدرس" in question:
        answer = "ما در خیابان انقلاب، پلاک ۲۲ قرار داریم."
    elif "سلام" in question:
        answer = "سلام! خوش اومدی 😊 چطور می‌تونم کمکت کنم؟"
    else:
        answer = "متوجه نشدم، لطفاً واضح‌تر بپرس 🌸"

    return jsonify({"answer": answer})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
