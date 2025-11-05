from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "🍽️ ربات سفارش‌گیر رستوران آنلاین فعال است!"

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data.get("question", "").lower()

    if "ساعت کاری" in question:
        answer = "⏰ ساعت کاری ما از ۱۲ ظهر تا ۱۲ شب است."
    elif "منو" in question:
        answer = "📜 منوی ما شامل پیتزا، برگر، پاستا و نوشیدنی‌های متنوع است."
    elif "آدرس" in question or "کجایید" in question:
        answer = "📍 ما در خیابان انقلاب، پلاک ۲۲ قرار داریم."
    elif "سلام" in question:
        answer = "سلام! 😊 خوش اومدی به رستوران ما. چه کمکی ازم برمیاد؟"
    elif "شماره" in question or "تماس" in question:
        answer = "📞 شماره تماس ما: ۰۲۱-۱۲۳۴۵۶۷۸"
    elif "رزرو" in question:
        answer = "برای رزرو میز لطفاً با شماره ۰۲۱-۱۲۳۴۵۶۷۸ تماس بگیرید یا از طریق وب‌سایت اقدام کنید."
    else:
        answer = "🤖 متوجه نشدم، لطفاً واضح‌تر بپرس 🌸"

    return jsonify({"answer": answer})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
