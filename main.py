import requests
import re
import time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# ---------------- CONFIG ----------------
BOT_TOKEN = "8281944831:AAGrz2zrLVLwdDd2BKISYUndRnD6yLn8pEE"

API_URL = "http://147.135.212.197/crapi/st/viewstats"
API_TOKEN = "RFdUREJBUzR9T4dVc49ndmFra1NYV5CIhpGVcnaOYmqHhJZXfYGJSQ=="

# ---------------- FETCH ----------------
def fetch_data():
    try:
        r = requests.get(API_URL, params={"token": API_TOKEN}, timeout=10)
        data = r.json()
        return data if isinstance(data, list) else []
    except:
        return []

# ---------------- START ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📱 Get Number", callback_data="get_number")]
    ]

    await update.message.reply_text(
        "✨ OTP Bot ✨\n\nGet number and receive OTP:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ---------------- BUTTON ----------------
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # ---------------- GET NUMBER ----------------
    if query.data == "get_number":
        data = fetch_data()

        if not data:
            await query.message.reply_text("❌ نمبر پیدا نشو!")
            return

        # اول available نمبر
        entry = data[0]
        number = entry[1]

        context.user_data["number"] = number

        keyboard = [
            [InlineKeyboardButton("📩 Get OTP", callback_data="get_otp")]
        ]

        await query.message.reply_text(
            f"📞 Your Number:\n{number}",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # ---------------- GET OTP ----------------
    elif query.data == "get_otp":
        number = context.user_data.get("number")

        if not number:
            await query.message.reply_text("❌ اول نمبر واخله!")
            return

        await query.message.reply_text("⏳ Waiting for OTP...")

        # loop for OTP
        for _ in range(15):
            data = fetch_data()

            for entry in data:
                phone = entry[1]
                message = entry[2]

                # فقط هماغه نمبر
                if phone == number:
                    otp = re.search(r"\b\d{4,8}\b", message)
                    if otp:
                        await query.message.reply_text(
                            f"✅ OTP:\n\n🔑 {otp.group()}"
                        )
                        return

            time.sleep(5)

        await query.message.reply_text("❌ OTP نه دی راغلی!")

# ---------------- MAIN ----------------
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(buttons))

print("🚀 Bot Running...")
app.run_polling(close_loop=False)
