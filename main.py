from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import json, os

TOKEN = "9254739622:AAE0QQFuVTqC51KaGKCxWIFAJKJCxrnWf6A"
CHANNEL_ID = "@ckspmenfess"
ADMIN_IDS = [7700854177, 1497040250]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Halo! Kirim menfess pake /menfess <pesan kamu>")

async def menfess(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    msg = update.message
    if msg.caption:
        text = msg.caption.replace("/menfess", "").strip()
    else:
        text = " ".join(context.args)
    source = msg
    if msg.reply_to_message and (msg.reply_to_message.photo or msg.reply_to_message.video or msg.reply_to_message.voice or msg.reply_to_message.audio or msg.reply_to_message.sticker or msg.reply_to_message.video_note or msg.reply_to_message.animation or msg.reply_to_message.document):
        source = msg.reply_to_message
    jenis = "teks"
    if source.photo:
        await context.bot.send_photo(chat_id=CHANNEL_ID, photo=source.photo[-1].file_id, caption=text)
        jenis = "foto"
    elif source.video:
        await context.bot.send_video(chat_id=CHANNEL_ID, video=source.video.file_id, caption=text)
        jenis = "video"
    elif source.voice:
        await context.bot.send_voice(chat_id=CHANNEL_ID, voice=source.voice.file_id, caption=text)
        jenis = "voice note"
    elif source.audio:
        await context.bot.send_audio(chat_id=CHANNEL_ID, audio=source.audio.file_id, caption=text)
        jenis = "lagu"
    elif source.sticker:
        await context.bot.send_sticker(chat_id=CHANNEL_ID, sticker=source.sticker.file_id)
        if text:
            await context.bot.send_message(chat_id=CHANNEL_ID, text=text)
        jenis = "sticker"
    elif source.video_note:
        await context.bot.send_video_note(chat_id=CHANNEL_ID, video_note=source.video_note.file_id)
        if text:
            await context.bot.send_message(chat_id=CHANNEL_ID, text=text)
        jenis = "video note"
    elif source.animation:
        await context.bot.send_animation(chat_id=CHANNEL_ID, animation=source.animation.file_id, caption=text)
        jenis = "gif"
    elif source.document:
        await context.bot.send_document(chat_id=CHANNEL_ID, document=source.document.file_id, caption=text)
        jenis = "file"
    else:
        if not text:
            await update.message.reply_text("Isi menfessnya mana? Contoh: /menfess halo")
            return
        await context.bot.send_message(chat_id=CHANNEL_ID, text=text)
    nama = f"@{user.username}" if user.username else user.first_name
    for admin_id in ADMIN_IDS:
        await context.bot.send_message(chat_id=admin_id, text=f"Menfess baru [{jenis}] dari {nama} (ID: {user.id}) :\n{text}")
    await update.message.reply_text("Menfess kamu udah terkirim!")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("menfess", menfess))
app.add_handler(MessageHandler(filters.PHOTO & filters.CaptionRegex(r"^/menfess"), menfess))
app.add_handler(MessageHandler(filters.VIDEO & filters.CaptionRegex(r"^/menfess"), menfess))
app.add_handler(MessageHandler(filters.AUDIO & filters.CaptionRegex(r"^/menfess"), menfess))
app.add_handler(MessageHandler(filters.ANIMATION & filters.CaptionRegex(r"^/menfess"), menfess))
app.add_handler(MessageHandler(filters.Document.ALL & filters.CaptionRegex(r"^/menfess"), menfess))
print("Bot jalan...")
app.run_polling()
