from pyrogram.types import *
from pyrogram.errors import FloodWait
from pyrogram import Client, filters, enums
from pyrogram.errors.exceptions.forbidden_403 import ChatWriteForbidden
from pyrogram.errors.exceptions.bad_request_400 import ChatAdminRequired, UserAdminInvalid

@Client.on_message(filters.command("mute"))
async def mute_user(_, message):
    is_admin = await admin_check(message)
    if not is_admin: return
    user_id, user_first_name = extract_user(message)
    try: await message.chat.restrict_member(user_id=user_id, permissions=ChatPermissions())                         
    except Exception as error: await message.reply_text(str(error))
    else:
        if str(user_id).lower().startswith("@"):
            await message.reply_text(f"👍🏻 {user_first_name} Lavender's mouth is shut! 🤐")
        else:
            await message.reply_text(f"👍🏻 Of lavender The mouth is closed! 🤐")
