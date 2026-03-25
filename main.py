import requests
import re
import time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# ---------------- CONFIG ----------------
BOT_TOKEN = "8281944831:AAGrz2zrLVLwdDd2BKISYUndRnD6yLn8pEE"

API_URL = "http://147.135.212.197/crapi/st/viewstats"
API_TOKEN = "RFdUREJBUzR9T4dVc49ndmFra1NYV5CIhpGVcnaOYmqHhJZXfYGJSQ=="

# ---------------- START ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📱 Get Number", callback_data="get_number")]
    ]

    await update.message.reply_text(
        "✨ Welcome OTP Bot ✨\n\nClick button to get number:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ---------------- BUTTON ----------------
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "get_number":
        number = "+1234567890"  # دلته خپل نمبر API سره وصل کړه

        context.user_data["number"] = number

        keyboard = [
            [InlineKeyboardButton("📩 Get OTP", callback_data="get_otp")]
        ]

        await query.message.reply_text(
            f"📞 Your Number:\n{number}",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "get_otp":
        await query.message.reply_text("⏳ Waiting for OTP...")

        # OTP fetch loop
        for _ in range(12):
            try:
                res = requests.get(API_URL, params={"token": API_TOKEN}, timeout=10)
                data = res.json()

                if isinstance(data, list):
                    for entry in data:
                        msg = entry[2]

                        otp = re.search(r"\b\d{4,8}\b", msg)
                        if otp:
                            await query.message.reply_text(
                                f"✅ OTP Code:\n\n🔑 {otp.group()}"
                            )
                            return

            except:
                pass

            time.sleep(5)

        await query.message.reply_text("❌ OTP not received!")

# ---------------- MAIN ----------------
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(buttons))

print("🚀 Bot Running...")
app.run_polling(close_loop=False)
