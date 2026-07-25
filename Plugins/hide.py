from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.enums import ChatMemberStatus

# ==========================================================
# 1. إعداد التعديل التلقائي لإضافة الزر لكافة ردود البوت
# ==========================================================

HIDE_BUTTON = InlineKeyboardButton("إخفاء ✖️", callback_data="hide_bot_msg")

# حفظ الدوال الأصلية لمكتبة Pyrogram
_orig_reply_text = Message.reply_text
_orig_send_message = Client.send_message
_orig_reply_photo = Message.reply_photo

def _add_hide_button(kwargs):
    """إضافة زر الإخفاء تلقائياً، مع الحفاظ على الأزرار السابقة إن وجدت"""
    reply_markup = kwargs.get("reply_markup")
    if reply_markup is None:
        kwargs["reply_markup"] = InlineKeyboardMarkup([[HIDE_BUTTON]])
    elif isinstance(reply_markup, InlineKeyboardMarkup):
        new_keyboard = list(reply_markup.inline_keyboard)
        new_keyboard.append([HIDE_BUTTON])
        kwargs["reply_markup"] = InlineKeyboardMarkup(new_keyboard)

async def custom_reply_text(self, text, *args, **kwargs):
    _add_hide_button(kwargs)
    return await _orig_reply_text(self, text, *args, **kwargs)

async def custom_send_message(self, chat_id, text, *args, **kwargs):
    _add_hide_button(kwargs)
    return await _orig_send_message(self, chat_id, text, *args, **kwargs)

async def custom_reply_photo(self, photo, *args, **kwargs):
    _add_hide_button(kwargs)
    return await _orig_reply_photo(self, photo, *args, **kwargs)

# استبدال الدوال الأصلية بالدوال المعدلة تلقائياً
Message.reply_text = custom_reply_text
Message.reply = custom_reply_text
Client.send_message = custom_send_message
Message.reply_photo = custom_reply_photo


# ==========================================================
# 2. معالج الضغط على الزر والتحقق من صلاحيات المدير/المشرف
# ==========================================================

@Client.on_callback_query(filters.regex("^hide_bot_msg$"))
async def handle_hide_message(client: Client, callback_query: CallbackQuery):
    chat = callback_query.message.chat
    user_id = callback_query.from_user.id

    # في المحادثات الخاصة: يمكن للمستخدم إخفاء الرسالة مباشرة
    if chat.type.name == "PRIVATE":
        await callback_query.message.delete()
        return

    # في المجموعات: التحقق من صلاحيات المستخدم
    try:
        member = await client.get_chat_member(chat.id, user_id)
        
        # السماح فقط لمالك المجموعة (OWNER) أو المشرفين (ADMINISTRATOR)
        if member.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]:
            await callback_query.message.delete()
        else:
            await callback_query.answer(
                "⚠️ هذا الزر مخصص للمشرفين والمدراء فقط!", 
                show_alert=True
            )
    except Exception:
        await callback_query.answer("تعذر التحقق من الصلاحيات.", show_alert=True)
