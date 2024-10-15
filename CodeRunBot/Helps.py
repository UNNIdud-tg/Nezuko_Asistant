from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Main menu with AI button
@Client.on_message(filters.command("helps"))
async def start_menu(client, message):
    # Main menu buttons with AI button
    buttons = [
        [InlineKeyboardButton("AI", callback_data="ai_menu")],
    ]
    
    # Main menu text
    main_menu_text = "⚡ Ready to explore? Click the button below to discover my commands!"
    
    # Image URL to display with the main menu
    image_url = "https://mangandi-2-0.onrender.com/eLSn.JPG"  # Replace with the actual image URL

    # Send the main menu with the image
    await client.send_photo(
        chat_id=message.chat.id,
        photo=image_url,
        caption=main_menu_text,
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# Inline button for AI menu
@Client.on_callback_query(filters.regex("ai_menu"))
async def ai_menu(client, callback_query):
    # AI Commands help buttons (including back button)
    buttons = [
        [InlineKeyboardButton("🔙 Back", callback_data="main_menu")]
    ]
    
    # AI Commands text
    ai_commands_text = """
    ⚡ **Commands:**

    - `/gpt4o <query>`: Get a response from GPT-4o Mini.
    - `/Claude <query>`: Get a response from Claude 3 Haiku.
    - `/mistral <query>`: Get a response from Mistral AI.
    - `/meta <query>`: Get a response from Meta Llama.
    - `/draw <query>`: Generate an image from text (image generation).
    - `/imagine <query>`: Similar to draw, image generation from text.
    - `/art <query>`: Create art using text (image generation).
    - `/bdraw <query>`: Generate an image using blackbox model.
    """
    
    # Image URL to display with the AI menu
    image_url = "https://mangandi-2-0.onrender.com/eLSn.JPG"  # Replace with actual image URL

    # Send AI commands with the image and buttons
    await client.send_photo(
        chat_id=callback_query.message.chat.id,
        photo=image_url,
        caption=ai_commands_text,
        reply_markup=InlineKeyboardMarkup(buttons)
    )
    await callback_query.answer()

# Command handler for returning to the main menu
@Client.on_callback_query(filters.regex("main_menu"))
async def back_to_main_menu(client, callback_query):
    # Main menu buttons
    buttons = [
        [InlineKeyboardButton("AI", callback_data="ai_menu")],
    ]
    
    # Main menu text
    main_menu_text = "⚡ **Welcome back! Please select an option below:**"
    
    # Image URL to display when returning to the main menu
    image_url = "https://mangandi-2-0.onrender.com/eLSn.JPG"  # Same or different image URL

    # Edit the message to show the main menu with the image
    await client.send_photo(
        chat_id=callback_query.message.chat.id,
        photo=image_url,
        caption=main_menu_text,
        reply_markup=InlineKeyboardMarkup(buttons)
    )
    await callback_query.answer()
    
