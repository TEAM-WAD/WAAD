from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types import AudioPiped
import asyncio

# ضع بياناتك هنا
api_id = 30357243 
api_hash = "9782c26101c502f026721b8e7993786c"

app = Client("music_bot", api_id=api_id, api_hash=api_hash)
call = PyTgCalls(app)

@app.on_message(filters.command("شغل") & filters.reply)
async def play(client, message):
    if message.reply_to_message.audio:
        # تحميل الملف الصوتي من المحادثة
        file_path = await message.reply_to_message.download()
        await message.reply("جاري التشغيل...")
        # تشغيل الملف
        await call.join_group_call(
            message.chat.id,
            AudioPiped(file_path)
        )

app.start()
call.start()
asyncio.get_event_loop().run_forever()
