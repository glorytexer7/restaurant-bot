from flask import Flask, request, jsonify

app = Flask(__name__)

# پاسخ ساده برای سوالات مشتری
def get_bot_response(message):
    message = message.lower()
    if "سلام" in message:
        return "سلام! خوش اومدی به رستوران عقاب طلایی 🦅 چطور می‌تونم کمکت کنم؟"
    elif "منو" in message or "چی دارید" in message:
        return "منوی ما شامل پیتزا، برگر، پاستا، سالاد و نوشابه هست 🍕🍔🍝🥗"
    elif "پیتزا" in message:
        return "پیتزای ما ترکیبی از پپرونی، قارچ، زیتون و سس مخصوصه 🍕"
    elif "ساعت" in message or "باز" in message:
        return "ما هر روز از ۱۰ صبح تا ۱۱ شب باز هستیم ⏰"
    elif "آدرس" in message:
        return "تهران، خیابان ولیعصر، نبش کوچه ۱۲۳ 📍"
    elif "شماره" in message or "تماس" in message:
        return "شماره تماس ما: ۰۲۱-۱۲۳۴۵۶۷۸ ☎️"
    elif "خداحافظ" in message or "مرسی" in message:
        return "خواهش می‌کنم 🌸 خوشحال شدم کمکت کنم!"
    else:
        return "متوجه نشدم 🤔 لطفاً واضح‌تر بپرس (مثلاً بنویس «منو چی دارید؟»)."

@app.route("/")
def home():
    return "🤖 ربات راهنمای رستوران فعال است!"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    bot_reply = get_bot_response(user_message)
    return jsonify({"reply": bot_reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
