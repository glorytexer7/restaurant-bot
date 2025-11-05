from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "🍽️ API ربات سفارش‌گیر رستوران آماده است!"})

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
