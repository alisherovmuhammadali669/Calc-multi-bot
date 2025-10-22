import re
import asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# --- Sozlamalar ---
TOKEN = "8279112441:AAEJAzpQUfBRUYy6l_pP9PggxoWZxTfRR5M"  # ⚠️ Tokenni bu yerga joylashtiring
VAQT = 1  # "Hisoblanmoqda..." xabari necha soniya turadi

# --- Foydalanuvchiga xabarlar ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "👋Assalomu alaykum! Men matematik amallarni yecha olaman.\n\n"
        "Men quyidagi amallarni bajara olaman:\n"
        "  ➕ Qo‘shish (+)\n"
        "  ➖ Ayirish (-)\n"
        "  ✖️ Ko‘paytirish (× yoki *)\n"
        "  ➗ Bo‘lish (÷ yoki /)\n\n"
        "📚Foydalanish qo‘llanmasini koʻrish uchun /help buyrugʻini yuboring."
    )
    await update.message.reply_text(msg)


# --- /help komandasi ---
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "📘Misol yuborish formatlari:\n"
        "1️⃣ 123 + 123\n"
        "2️⃣ 123 + 123 - 123 × 123\n"
        "3️⃣ (123 + 123) ÷ (123 - 123) × 123\n\n"
        "⚠️Hech qachon ↩️ tugmasini bosmang!"
    )
    await update.message.reply_text(msg)


# --- Xavfsiz hisoblash funksiyasi ---
def safe_calculate(expr: str):
    """Matematik ifodani xavfsiz hisoblaydi."""
    expr = (
        expr.replace("×", "*")
            .replace("x", "*")
            .replace("X", "*")
            .replace("÷", "/")
    )

    if not re.match(r'^[0-9+\-*/().\s]+$', expr):
        return None

    try:
        return eval(expr, {"__builtins__": None}, {})
    except Exception:
        return None


# --- Natijani formatlash ---
def format_number(n):
    if n is None:
        return None
    return str(int(n)) if abs(n - int(n)) < 1e-12 else f"{n:.10g}"


# --- Hisoblash ---
async def calculate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    expr = update.message.text.strip()
    result = safe_calculate(expr)

    if result is None:
        await update.message.reply_text("❌Xato ifoda!")
        return

    # "Hisoblanmoqda..." xabarini yuborish
    hisob_msg = await update.message.reply_text("⏳Hisoblanmoqda...")

    # Kutish (asinxron)
    await asyncio.sleep(VAQT)

    # "Hisoblanmoqda..." xabarini o‘chirish
    await hisob_msg.delete()

    # Natijani chiqarish
    await update.message.reply_text(f"Javob: {format_number(result)}✅")


# --- Noma’lum buyruqlar ---
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❓Nomaʼlum buyruq.")


# --- Asosiy funksiya ---
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, calculate))
    app.add_handler(MessageHandler(filters.COMMAND, unknown))

    print("🤖 Bot ishga tushdi...")
    app.run_polling()


if __name__ == "__main__":
    main()