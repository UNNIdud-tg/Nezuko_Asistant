from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import Client, filters , enums

@Client.on_message(filters.command('start'))
async def ai_generate_private(client, message):
    buttons = [[
        InlineKeyboardButton("Support", url="https://t.me/MRXSUPPORTS")
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    # Fixed the misplaced parenthesis
    await message.reply_text(
        text=f"Hey {message.from_user.mention}\n 𝐇𝐞𝐲 𝐭𝐡𝐞𝐫𝐞! 𝐌𝐲 𝐧𝐚𝐦𝐞 𝐢𝐬 𝐕𝐞𝐠𝐞𝐭𝐚 - 𝐈'𝐦 𝐡𝐞𝐫𝐞 𝐭𝐨 𝐡𝐞𝐥𝐩 𝐲𝐨𝐮! \n\n 𝐩𝐫𝐨𝐯𝐢𝐝𝐞𝐝 𝐛𝐲 @MRXSUPPORTS", 
        reply_markup=reply_markup
    )
