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
        InlineKeyboardButton("Add me to your group", url="http://t.me/NezukoRobot?startgroup=true")  # New button on a separate row
    ]]
    
    reply_markup = InlineKeyboardMarkup(buttons)
    
    # Check if the bot is started in a private chat (DM)
    if message.chat.type == enums.ChatType.PRIVATE:
        # Message for DM (Private Chat)
        await message.reply_photo(
            photo='https://mangandi-2-0.onrender.com/7EfZ.JPG',  # Replace with an actual image URL if needed
            caption="Hey there! My name is Nezuko - I'm here to help you! Use /help to find out more about how to use me to my full potential.\n\nJoin my @MRXSUPPORTS to get information on all the latest updates.",
            reply_markup=reply_markup
        )

    # Check if the bot is started in a group or supergroup
    elif message.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        # Message for Group Chat
        await message.reply(
            "Greetings! Nezuko here. Ready to explore and engage? Type /help for options. Let’s begin!",
            reply_markup=reply_markup
        )

    # Sleep to avoid flood wait
    await asyncio.sleep(2)
    if not await db.get_chat(message.chat.id):
        pass  # Handle this case if necessary

@Client.on_message(filters.command("help"))
async def help(client, message):
    await message.reply_text(HELP)
