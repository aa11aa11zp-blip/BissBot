import requests
import sqlite3
import re
import time
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# ---------------- LOGGING ----------------
logging.basicConfig(level=logging.INFO)

# ---------------- CONFIG ----------------
BOT_TOKEN = "8281944831:AAGrz2zrLVLwdDd2BKISYUndRnD6yLn8pEE"
API_TOKEN = "RFdUREJBUzR9T4dVc49ndmFra1NYV5CIhpGVcnaOYmqHhJZXfYGJSQ=="
API_URL = "http://147.135.212.197/crapi/st/viewstats"

ADMIN_ID = 1316375131
CHANNELS = ["@ProTech43", "@HematTech", "@Pro43Zone", "@SQ_Botz"]

# ---------------- DATABASE ----------------
conn = sqlite3.connect("data.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    referrals INTEGER DEFAULT 0,
    invited_by INTEGER
)
""")
conn.commit()

# ---------------- FUNCTIONS ----------------
async def check_join(user_id, context):
    for ch in CHANNELS:
        try:
            member = await context.bot.get_chat_member(ch, user_id)
            if member.status in ["left", "kicked"]:
                return False
        except:
            return False
    return True

def add_user(user_id, ref=None):
    cur.execute("INSERT OR IGNORE INTO users (user_id, invited_by) VALUES (?,?)", (user_id, ref))
    conn.commit()

    if ref and ref != user_id:
        cur.execute("UPDATE users SET referrals = referrals + 1 WHERE user_id=?", (ref,))
        conn.commit()

def get_refs(user_id):
    cur.execute("SELECT referrals FROM users WHERE user_id=?", (user_id,))
    row = cur.fetchone()
    return row[0] if row else 0

# ---------------- START ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    args = context.args

    ref = int(args[0]) if args else None
    add_user(user.id, ref)

    if not await check_join(user.id, context):
        buttons = [
            [InlineKeyboardButton("📢 Join 1", url="https://t.me/ProTech43")],
            [InlineKeyboardButton("📢 Join 2", url="https://t.me/HematTech")],
            [InlineKeyboardButton("📢 Join 3", url="https://t.me/Pro43Zone")],
            [InlineKeyboardButton("📢 Join 4", url="https://t.me/SQ_Botz")]
        ]
        await update.message.reply_text(
            "⚠️ ټول چینلونه Join کړه بیا Start وکړه!",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
        return

    keyboard = [
        [InlineKeyboardButton("📱 Number واخله", callback_data="get")],
        [InlineKeyboardButton("👥 ریفیرل", callback_data="ref")]
    ]

    await update.message.reply_text(
        "✨ Welcome OTP Bot ✨\n\nیو انتخاب وکړه:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ---------------- BUTTON ----------------
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    if query.data == "get":
        refs = get_refs(user_id)

        if refs < 2:
            link = f"https://t.me/YOUR_BOT?start={user_id}"
            await query.message.reply_text(
                f"❌ 2 ریفیرل ته ضرورت دی!\n\n🔗 لینک:\n{link}"
            )
            return

        cur.execute("UPDATE users SET referrals = referrals - 2 WHERE user_id=?", (user_id,))
        conn.commit()

        await query.message.reply_text("📩 سرویس ولیکه (WhatsApp / Telegram)")
        context.user_data["wait_service"] = True

    elif query.data == "ref":
        refs = get_refs(user_id)
        link = f"https://t.me/YOUR_BOT?start={user_id}"

        await query.message.reply_text(
            f"👥 ستا ریفیرل: {refs}\n\n🔗 لینک:\n{link}"
        )

# ---------------- API ----------------
def fetch_sms():
    try:
        r = requests.get(API_URL, params={"token": API_TOKEN}, timeout=15)
        data = r.json()
        return data if isinstance(data, list) else []
    except Exception as e:
        print("API ERROR:", e)
        return []

# ---------------- MESSAGE ----------------
async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("wait_service"):
        context.user_data["wait_service"] = False

        number = "+1234567890"
        context.user_data["number"] = number

        await update.message.reply_text(
            f"📞 نمبر:\n{number}\n\n⏳ OTP ته انتظار..."
        )

        # OTP check loop
        for _ in range(12):
            data = fetch_sms()

            for entry in data:
                try:
                    msg = entry[2]
                except:
                    continue

                otp = re.search(r"\b\d{4,8}\b", msg)
                if otp:
                    await update.message.reply_text(
                        f"✅ OTP:\n\n🔑 {otp.group()}"
                    )
                    return

            time.sleep(5)

        await update.message.reply_text("❌ OTP ونه راغی!")

# ---------------- BROADCAST ----------------
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        return

    text = " ".join(context.args)

    cur.execute("SELECT user_id FROM users")
    users = cur.fetchall()

    for u in users:
        try:
            await context.bot.send_message(chat_id=u[0], text=text)
        except:
            pass

    await update.message.reply_text("✅ Broadcast وشو")

# ---------------- MAIN ----------------
app = ApplicationBuilder().token(BOT_TOKEN).concurrent_updates(True).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(buttons))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message))
app.add_handler(CommandHandler("broadcast", broadcast))

print("🚀 Bot Running...")
app.run_polling(close_loop=False) 
