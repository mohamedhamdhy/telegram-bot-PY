import os
from telegram import Update
from telegram.ext import ContextTypes
from database import SessionLocal
from models import Note


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome! Send me notes, documents, images, or videos and I'll store them."
    )


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    session = SessionLocal()
    user_id = update.message.from_user.id
    text = update.message.text

    note = Note(user_id=user_id, file_type="text", text_content=text)
    session.add(note)
    session.commit()
    session.close()

    await update.message.reply_text("Your text note has been saved.")


async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    session = SessionLocal()
    user_id = update.message.from_user.id

    document = update.message.document
    file_name = document.file_name
    file_id = document.file_id

    file = await context.bot.get_file(file_id)
    file_bytes = await file.download_as_bytearray()

    note = Note(
        user_id=user_id,
        file_name=file_name,
        file_type="document",
        content=file_bytes,
    )
    session.add(note)
    session.commit()
    session.close()

    await update.message.reply_text(f"Document '{file_name}' saved successfully.")


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    session = SessionLocal()
    user_id = update.message.from_user.id

    photo = update.message.photo[-1]
    file_id = photo.file_id

    file = await context.bot.get_file(file_id)
    file_bytes = await file.download_as_bytearray()

    note = Note(
        user_id=user_id,
        file_name=None,
        file_type="image",
        content=file_bytes,
    )
    session.add(note)
    session.commit()
    session.close()

    await update.message.reply_text("Photo saved successfully.")


async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    session = SessionLocal()
    user_id = update.message.from_user.id

    video = update.message.video
    file_id = video.file_id
    file_name = video.file_name if video.file_name else "video"

    file = await context.bot.get_file(file_id)
    file_bytes = await file.download_as_bytearray()

    note = Note(
        user_id=user_id,
        file_name=file_name,
        file_type="video",
        content=file_bytes,
    )
    session.add(note)
    session.commit()
    session.close()

    await update.message.reply_text(f"Video '{file_name}' saved successfully.")
