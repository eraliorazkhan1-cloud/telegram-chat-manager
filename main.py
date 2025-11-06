from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ChatMemberUpdated
from aiogram import F
import asyncio
import logging
import os
from keep_alive import keep_alive  # ← это держит бота живым

# === ТОКЕН ИЗ СЕКРЕТОВ ===
API_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# === БАЗА ===
stats = {"messages": 0, "users": set()}
BAD_WORDS = ["дурак", "идиот", "дебил", "сука", "блять", "пидор"]

# === ПРИВЕТСТВИЕ ===
@dp.my_chat_member(ChatMemberUpdated.filter(F.new_chat_member.status == "member"))
async def on_join(event: ChatMemberUpdated):
    user = event.new_chat_member.user
    await event.answer(f"👋 Привет, {user.first_name}! Без мата и спама! 🚀")
    stats["users"].add(user.id)

# === АНТИМАТ ===
@dp.message(F.text)
async def check(message: types.Message):
    if message.text and any(word in message.text.lower() for word in BAD_WORDS):
        await message.delete()
        await message.answer(f"⚠️ @{message.from_user.username}, мат запрещён!")
        return
    stats["messages"] += 1
    stats["users"].add(message.from_user.id)

# === КОМАНДЫ ===
@dp.message(Command("stats"))
async def stats_cmd(message: types.Message):
    await message.answer(f"📊 Участников: {len(stats['users'])}\n💬 Сообщений: {stats['messages']}")

@dp.message(Command("help"))
async def help_cmd(message: types.Message):
    await message.answer("🔥 /stats — статистика\n/start — привет\nМат = бан!")

# === ЗАПУСК ===
async def main():
    keep_alive()  # ← 24/7 магия
    print("🚀 Бот 24/7 запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())