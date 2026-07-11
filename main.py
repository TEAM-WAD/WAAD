import os
import sys
import asyncio

# دالة فحص وإنشاء الإعدادات تلقائياً من الترمينال
def check_config():
    config_file = "config.py"
    if not os.path.exists(config_file):
        print("📥 [إعداد السورس لأول مرة] يرجى إدخال البيانات المطلوبة بالترمينال:")
        bot_token = input("🤖 أدخل توكن البوت (Bot Token): ").strip()
        api_id = input("🆔 أدخل الـ API ID (من موقع my.telegram.org): ").strip()
        api_hash = input("🔑 أدخل الـ API HASH: ").strip()
        ass_session = input("📱 أدخل كود جلسة الحساب المساعد (Telethon String Session): ").strip()
        dev_id = input("👑 أدخل أيدي المطور الأساسي (Developer ID): ").strip()

        with open(config_file, "w", encoding="utf-8") as f:
            f.write(f'BOT_TOKEN = "{bot_token}"\n')
            f.write(f'API_ID = {api_id}\n')
            f.write(f'API_HASH = "{api_hash}"\n')
            f.write(f'ASS_SESSION = "{ass_session}"\n')
            f.write(f'DEV_ID = {dev_id}\n')
        print("✅ تم حفظ الإعدادات بنجاح في ملف config.py!\n🔄 جاري تشغيل السورس الآن...")

# تشغيل الفحص قبل أي استدعاء ثانٍ
check_config()

# استدعاء المكاتب بعد التأكد من الإعدادات
from telethon import TelegramClient, events, Button
from telethon.sessions import StringSession
from telethon.tl.types import MessageMediaDocument
from pytgcalls import PyTgCalls
from pytgcalls.types import AudioImagePiped
from pytgcalls.exceptions import AlreadyJoinedError
from yt_dlp import YoutubeDL
import config

print("⚡ جاري الاتصال بالتليجرام وتشغيل الحساب المساعد...")

# تشغيل البوت المساعد والأساسي
bot = TelegramClient('music_bot', config.API_ID, config.API_HASH).start(bot_token=config.BOT_TOKEN)
assistant = TelegramClient(StringSession(config.ASS_SESSION), config.API_ID, config.API_HASH)
call_py = PyTgCalls(assistant)

def get_yt_audio(query):
    if not os.path.exists("downloads"):
        os.makedirs("downloads")
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloads/%(id)s.%(ext)s',
        'noplaylist': True,
        'quiet': True,
    }
    with YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(f"ytsearch:{query}", download=True)
            video = info['entries'][0] if 'entries' in info and len(info['entries']) > 0 else info
            return ydl.prepare_filename(video), video['title']
        except Exception as e:
            print(f"Error YoutubeDL: {e}")
            return None, None

async def start_services():
    await assistant.start()
    await call_py.start()
    print("🚀 السورس شغال وجاهز لاستقبال الأوامر!")

loop = asyncio.get_event_loop()
loop.create_task(start_services())

# أمر التشغيل من اليوتيوب
@bot.on(events.NewMessage(pattern=r"^\.(تشغيل|شغل) (.*)"))
async def play_yt(event):
    chat_id = event.chat_id
    query = event.pattern_match.group(2)
    msg = await event.reply("🔍 جاري البحث والتحميل من اليوتيوب...")
    
    file_path, title = await loop.run_in_executor(None, get_yt_audio, query)
    if not file_path:
        return await msg.edit("❌ لم يتم العثور على المقطع الصوتي.")
        
    await msg.edit(f"🔄 جاري انضمام المساعد وتشغيل:\n🎵 **{title}**")
    try:
        await call_py.join_group_call(chat_id, AudioImagePiped(file_path))
    except AlreadyJoinedError:
        await call_py.change_stream(chat_id, AudioImagePiped(file_path))
    except Exception as e:
        return await msg.edit(f"❌ فشل تشغيل المكالمة: {e}")

    buttons = [
        [Button.inline("⏸️ إيقاف مؤقت", data="pause"), Button.inline("▶️ استئناف", data="resume")],
        [Button.inline("⏹️ مغادرة", data="stop")]
    ]
    await msg.edit(f"🎶 **تم التشغيل بنجاح**\n🎵 المقطع: {title}", buttons=buttons)

# أمر تشغيل ملف من التليجرام
@bot.on(events.NewMessage(pattern=r"^\.(تشغيل_ملف|شغل_ملف)"))
async def play_file(event):
    chat_id = event.chat_id
    if not event.is_reply:
        return await event.reply("❌ يرجى الرد على ملف صوتی.")
    reply_msg = await event.get_reply_message()
    if not reply_msg.media or not isinstance(reply_msg.media, MessageMediaDocument):
        return await event.reply("❌ هذا ليس ملفاً صوتياً.")
        
    msg = await event.reply("📥 جاري تحميل الملف...")
    file_path = await reply_msg.download_media(file="downloads/")
    await msg.edit("🔄 جاري التشغيل في المكالمة...")
    try:
        await call_py.join_group_call(chat_id, AudioImagePiped(file_path))
    except AlreadyJoinedError:
        await call_py.change_stream(chat_id, AudioImagePiped(file_path))
    except Exception as e:
        return await msg.edit(f"❌ خطأ: {e}")
    await msg.edit("🎶 تم تشغيل الملف بنجاح!")

# التحكم بالأزرار
@bot.on(events.CallbackQuery())
async def inline_buttons_handler(event):
    chat_id = event.chat_id
    data = event.data.decode('utf-8')
    try:
        if data == "pause":
            await call_py.pause_stream(chat_id)
            await event.answer("⏸️ تم الإيقاف المؤقت", alert=True)
        elif data == "resume":
            await call_py.resume_stream(chat_id)
            await event.answer("▶️ تم الاستئناف", alert=True)
        elif data == "stop":
            await call_py.leave_group_call(chat_id)
            await event.edit("⏹️ تم إنهاء البث ومغادرة المساعد.")
    except Exception:
        await event.answer("⚠️ لا توجد مكالمة نشطة.")

bot.run_until_disconnected()
