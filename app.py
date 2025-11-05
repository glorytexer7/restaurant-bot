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
  background-color: #f8f8f8;
  text-align: center;
  padding: 30px;
  direction: rtl;
}
.chat-box {
  background: white;
  width: 100%;
  max-width: 500px;
  margin: 0 auto;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.2);
  padding: 20px;
}
input {
  width: 80%;
  padding: 10px;
  border-radius: 6px;
  border: 1px solid #ccc;
}
button {
  padding: 10px 15px;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}
button:hover {
  background-color: #218838;
}
.message {
  margin-top: 15px;
  padding: 10px;
  background-color: #eee;
  border-radius: 6px;
}
.answer {
  background-color: #d1e7dd;
}
</style>
</head>
<body>
<h2>🍽️ ربات سفارش‌گیر رستوران</h2>
<div class="chat-box">
  <div id="chat"></div>
  <br>
  <input type="text" id="question" placeholder="سوال خود را بنویسید...">
  <button onclick="sendQuestion()">ارسال</button>
</div>

<script>
async function sendQuestion() {
  const q = document.getElementById("question").value;
  if (!q) return;
  const chat = document.getElementById("chat");

  chat.innerHTML += `<div class='message'>👤 ${q}</div>`;

  const res = await fetch("/ask", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({question: q})
  });
  const data = await res.json();

  chat.innerHTML += `<div class='message answer'>🤖 ${data.answer}</div>`;
  document.getElementById("question").value = "";
}
</script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_PAGE)

@app.route('/ask', methods=['GET', 'POST'])
def ask():
    if request.method == 'GET':
        return jsonify({"message": "برای استفاده از این API از متد POST استفاده کنید."})

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
