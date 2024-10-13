from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from utils.message import *
from pyrogram import Client, filters , enums

@Client.on_message(filters.command('start'))
async def ai_generate_private(client, message):
    buttons = [[
        InlineKeyboardButton("Support", url="https://t.me/MRXSUPPORTS"),
        InlineKeyboardButton("Add me to your group", url="http://t.me/NezukoRobot?startgroup=true")
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    
    # Added line breaks before the buttons for visual separation
    await message.reply_text(
        text=f"Hey {message.from_user.mention}\n Hey there! My name is Nezuko - I'm here to help you! Use /help to find out more about how to use me to my full potential.\n\nJoin my @MRXSUPPORTS to get information on all the latest updates.\n\n\n",  # Added extra line breaks
        reply_markup=reply_markup
    )
    

@Client.on_message(filters.command("help"))
async def help(client, message):
    await message.reply_text(HELP)
    
