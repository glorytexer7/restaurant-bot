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
  font-family: sans-serif;
  background-color: #f0f0f0;
  direction: rtl;
  text-align: center;
  padding: 40px;
}
.chat-box {
  background: white;
  width: 100%;
  max-width: 500px;
  margin: 0 auto;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.2);
  padding: 20px;
  max-height: 500px;
  overflow-y: auto;
}
input {
  width: 80%;
  padding: 10px;
  border-radius: 6px;
  border: 1px solid #ccc;
  margin-top: 10px;
}
button {
  padding: 10px 15px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}
button:hover {
  background-color: #0056b3;
}
.message {
  margin-top: 10px;
  padding: 10px;
  background-color: #eee;
  border-radius: 6px;
  text-align: left;
  word-wrap: break-word;
}
.answer {
  background-color: #d1e7dd;
}
</style>
</head>
<body>

<h2>🍔 ربات سفارش‌گیر رستوران آنلاین</h2>

<div class="chat-box" id="chat"></div>

<input type="text" id="question" placeholder="سوال خود را بنویسید...">
<button onclick="sendQuestion()">ارسال</button>

<script>
async function sendQuestion() {
  const q = document.getElementById("question").value;
  if (!q) return;

  const chat = document.getElementById("chat");
  chat.innerHTML += `<div class='message'>👤 ${q}</div>`;

  try {
    const res = await fetch("/ask", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({question: q})
    });

    if (!res.ok) throw new Error("خطا در دریافت پاسخ");

    const data = await res.json();
    chat.innerHTML += `<div class='message answer'>🤖 ${data.answer}</div>`;

    // اسکرول خودکار به پایین
    chat.scrollTop = chat.scrollHeight;

  } catch (err) {
    chat.innerHTML += `<div class='message answer'>⚠️ خطا: ${err.message}</div>`;
  }

  document.getElementById("question").value = "";
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

    # پاسخ‌های ربات
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
