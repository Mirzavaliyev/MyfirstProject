from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram.constants import ParseMode

API_TOKEN = 'YOUR_API_TOKEN'  # O'zingizning API token'ni kiriting
ADMIN_ID = 'YOUR_ADMIN_ID'  # O'zingizning admin ID ni kiriting

# Botni boshlash
async def start(update: Update, context):
    user = update.message.from_user
    chat_id = update.message.chat_id

    if chat_id != int(ADMIN_ID):
        start_message = "🤖 Bot ishlashni boshladi! Guruhga qo'shilganingizda xabar yuborishingiz mumkin."
        await context.bot.send_message(chat_id=chat_id, text=start_message)
    else:
        await context.bot.send_message(chat_id=chat_id, text="🤗 Salom adminstrator")

# Guruhdagi a'zolarni tekshirish
async def check_user(update: Update, context):
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id

    # Faqat guruhda xabar yuborish
    if update.message.chat.type == 'private':
        await update.message.reply("Bot faqat guruhda ishlaydi.")
        return

    # Agar foydalanuvchi guruhga a'zo bo'lmasa, ularni xabar yuborishdan to'xtatish
    if not await check_member(update, user_id):
        await update.message.reply("Siz guruhga a'zo bo'lmagansiz, shuning uchun xabar yubora olmaysiz.\nOdam qo'shish uchun guruhga a'zo bo'ling.")
        return

    # Agar foydalanuvchi guruhga a'zo bo'lsa, qo'shilgan odamlar sonini ko'rsatish
    num_members = await get_member_count(update)
    await update.message.reply(f"Guruhda {num_members} ta a'zo bor.\nXabar yuborishda davom eting!")

# Guruhdagi foydalanuvchining a'zoligini tekshirish
async def check_member(update: Update, user_id: int):
    chat_id = update.message.chat_id
    member = await update.message.chat.get_member(user_id)
    return member.status in ['member', 'administrator', 'creator']

# Guruhdagi umumiy a'zolar sonini olish
async def get_member_count(update: Update):
    chat_id = update.message.chat_id
    chat = await update.message.chat.get_chat()
    return chat.members_count

# Asosiy handler
async def main():
    application = Application.builder().token(API_TOKEN).build()

    # Komanda handlerlari
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_user))

    await application.run_polling()

if __name__ == '__main__':
    import asyncio

    # Aslida asyncio.run() ishlamadi, bu holda quyidagi kodni ishlatamiz:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
git config --global user.name "Mirzavaliyev"
git config --global user.email "shavkatziyo98@gmail.com"
