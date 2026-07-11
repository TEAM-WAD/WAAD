import asyncio
from pytgcalls import PyTgCalls, idle
from pytgcalls.types import AudioPiped
from pyrogram import Client, filters

# ضع بياناتك الحقيقية هنا بدلاً من الأرقام
api_id = 30357243 
api_hash = "9782c26101c502f026721b8e7993786c"

app = Client("music_bot", api_id=api_id, api_hash=api_hash)
call = PyTgCalls(app)

@app.on_message(filters.command("شغل"))
async def play(client, message):
    if len(message.command) < 2:
        await message.reply("يرجى كتابة اسم الأغنية بعد الأمر")
        return
    query = message.text.split(" ", 1)[1]
    await message.reply("جاري التشغيل...")
    await call.join_group_call(
        message.chat.id, 
        AudioPiped(f"ytsearch:{query}", ydl_opts={'cookiefile': 'cookies.txt'})
    )

app.start()
call.start()
idle()
