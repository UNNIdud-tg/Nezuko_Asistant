from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Command handler for help with image
@Client.on_message(filters.command("helps"))
async def help_command(client, message):
    # Inline buttons for the main menu
    buttons = [
        [InlineKeyboardButton("🧠 AI Module", callback_data="ai_module")],
    ]
    
    # Image URL or file path (you can replace this with a local image path or a URL)
    image_url = "https://mangandi-2-0.onrender.com/7EfZ.JPG"
    
    # Send the image with the buttons and a description
    await client.send_photo(
        chat_id=message.chat.id,
        photo=image_url,  # Replace with your actual image URL or local path
        caption="Welcome to the Help Menu! Choose a module:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# Callback query handler
@Client.on_callback_query()
async def button_callback(client, callback_query):
    data = callback_query.data

    if data == "ai_module":
        # Display AI Module buttons with commands
        ai_buttons = [
            [InlineKeyboardButton("GPT-4o Mini", callback_data="gpt4o")],
            [InlineKeyboardButton("Claude 3 Haiku", callback_data="claude")],
            [InlineKeyboardButton("Mistral AI", callback_data="mistral")],
            [InlineKeyboardButton("Meta Llama", callback_data="meta_llama")],
        ]
        
        await callback_query.message.edit_text(
            "Choose an AI model:",
            reply_markup=InlineKeyboardMarkup(ai_buttons)
        )

    elif data == "gpt4o":
        await callback_query.message.edit_text("Use the command: /gpt4o  for GPT-4o Mini.")
    elif data == "claude":
        await callback_query.message.edit_text("Use the command: /Claude  for Claude 3 Haiku.")
    elif data == "mistral":
        await callback_query.message.edit_text("Use the command: /mistral  for Mistral AI.")
    elif data == "meta_llama":
        await callback_query.message.edit_text("Use the command: /meta  for Meta Llama.")
    
    await callback_query.answer()
