from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from utils.message import *
from pyrogram import Client, filters, enums

@Client.on_message(filters.command('start'))
async def ai_generate_private(client, message):
    # First row: Horizontal alignment of two buttons
    buttons = [[
        InlineKeyboardButton("Support", url="https://t.me/MRXSUPPORTS")
    ],
    # Second row: Button below the first row
    [
        InlineKeyboardButton("Add me to your group", url="http://t.me/NezukoRobot?startgroup=true") # New button on a separate row
    ]]
    
    reply_markup = InlineKeyboardMarkup(buttons)
    
    # Using reply_photo to send an image with a caption
    await message.reply_photo(
        photo='https://mangandi-2-0.onrender.com/7EfZ.JPG',  # Replace with the actual image URL
        caption=f"Hey {message.from_user.mention}\n Hey there! My name is Nezuko - I'm here to help you! Use /help to find out more about how to use me to my full potential.\n\nJoin my @MRXSUPPORTS to get information on all the latest updates.",
        reply_markup=reply_markup
    )
