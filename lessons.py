import asyncio
import json
from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ChatType
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties
from pathlib import Path

API_TOKEN = "8124116225:AAEXXNH6-Mk806oAFCSNarEGUPVye0qtiHc"
ADMIN_ID = 5922081119

GROUPS_FILE = "groups.json"

def load_groups():
    if Path(GROUPS_FILE).exists():
        with open(GROUPS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_groups(groups):
    with open(GROUPS_FILE, 'w') as f:
        json.dump(groups, f)


bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

@dp.message(Command("add"))
async def add_group(message: Message):
    if message.chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP, ChatType.CHANNEL]:
        await message.answer("Bu buyruq faqat guruhda ishlaydi.")
        return

    groups = load_groups()
    if message.chat.id not in groups:
        groups.append(message.chat.id)
        save_groups(groups)
        await message.answer("Guruh ro'yxatga qo‘shildi!")
    else:
        await message.answer("Bu guruh allaqachon ro'yxatda bor.")

@dp.message(Command("reklama"))

async def broadcast(message: Message):
    if message.chat.type != ChatType.PRIVATE:
        await message.reply("Reklama faqat shaxsiy chatda yuboriladi.")
        return

    if not message.reply_to_message:
        await message.answer("Reklama yuborish uchun reklama xabaringizga reply qilib yuboring: /broadcast")
        return

    groups = load_groups()
    count = 0
    for gid in groups:
        try:
            await bot.send_message(chat_id=gid, text=message.reply_to_message.text)
            count += 1
        except Exception as e:
            print(f"❌ Yuborib bo‘lmadi ({gid}):", e)

    await message.answer(f"Reklama {count} ta guruhga yuborildi.")


async def main():
    print("Bot ishladi ")

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
