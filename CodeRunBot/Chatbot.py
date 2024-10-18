import json
import os
import uuid
import logging
from pyrogram import Client, filters, types, enums
import aiohttp
import asyncio

# Path for JSON file
DATA_FILE = "chatbot_data.json"

# Logging setup for application-wide debugging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Load existing data from the JSON file
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    return {}

# Save data to the JSON file
def save_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

# Initialize the chatbot data
chatbot_data = load_data()

# Function to generate unique user IDs
def id_generator() -> str:
    return str(uuid.uuid4())

# Function to get chatbot responses and store them in the JSON file
async def get_response(user_id: str, messages: list) -> str:
    url = "https://www.blackbox.ai/api/chat"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    data = {
        "messages": messages,  
        "user_id": user_id,
        "codeModelMode": True,
        "agentMode": {
            "mode": True,
            "id": "NezukoKamado3SQbPzE",  # Agent ID
            "name": "Nezuko Kamado"  # Character Name
        },
        "trendingAgentMode": {}
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data, headers=headers) as response:
                if response.status == 200:
                    response_text = await response.text()

                    # Store the response in chatbot_data and save to the JSON file
                    chatbot_data[user_id] = messages[0]['content']  # Store the user message
                    chatbot_data[f"{user_id}_response"] = response_text.strip()  # Store the bot response
                    save_data(chatbot_data)

                    return response_text.strip()
                else:
                    return "⚠️ Unable to get a response from the chatbot."

    except Exception as e:
        logger.error(f"Error in get_response: {str(e)}")
        return f"❌ Something went wrong: {str(e)}"

# Pyrogram bot credentials
api_id = "27408015"  # Replace with your API ID
api_hash = "2f07e7c921c8d2b982df12d65a46ca46"  # Replace with your API Hash
bot_token = "7424717855:AAGzjRLuJLRNh0YoOhCRvDVI5kymDQfEvoA"  # Replace with your bot token

# Initialize Pyrogram client
app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Command to set the chatbot's behavior
@Client.on_message(filters.command("chatbot"))
async def chatbot_command(client, message):
    chat_id = str(message.chat.id)  # Use chat_id to store enable/disable status
    admin_ids = []
    ok = False

    if message.chat.type == enums.ChatType.PRIVATE:
        ok = True
    else:
        async for mem in client.get_chat_members(
            chat_id=message.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS
        ):
            admin_ids.append(mem.user.id)
        if message.from_user.id in admin_ids:
            ok = True

    if not ok:
        return await message.reply_text(
            "Sorry, you're not authorized to do this. Only admins can!"
        )

    return await message.reply_text(
        text="⚡ Chat Bot Settings",
        reply_markup=types.InlineKeyboardMarkup([[
            types.InlineKeyboardButton(
                text="🟢", callback_data=f"chatbot:enable:{message.from_user.id}:{chat_id}"
            ),
            types.InlineKeyboardButton(
                text="🔴", callback_data=f"chatbot:disable:{message.from_user.id}:{chat_id}"
            )
        ]])
    )

# Check if chatbot is enabled before replying
@Client.on_message(group=33)
async def chatbot_reply(client, message):
    chat_id = str(message.chat.id)
    
    # Check if chatbot is enabled in the current chat
    if chatbot_data.get(f"{chat_id}_status") != "enabled":
        return  # Do nothing if chatbot is disabled

    reply = message.reply_to_message
    if reply and reply.from_user and reply.from_user.id == client.me.id:
        prompt = message.text
        await client.send_chat_action(chat_id, enums.ChatAction.TYPING)
        msg = await message.reply_text("✨")     
        user_id = id_generator()
        messages = [{"role": "user", "content": prompt}]
        response = await get_response(user_id, messages)
        cleaned_response_text = response.replace('$v=undefined-rv1$@$(smirking)', '')
        text = cleaned_response_text.strip()[2:]       
        await msg.edit_text(text)

@Client.on_callback_query(filters.regex(r"^chatbot"))
async def chatbot_callback(client, query):
    """Handles enable/disable chatbot via inline keyboard."""
    user_id = int(query.data.split(':')[2])
    mod = query.data.split(':')[1]
    chat_id = query.data.split(':')[3]  # Get chat_id from the callback data
    m = query.message
    
    if query.from_user.id != user_id:
        return await query.answer(
            text="This is not requested by you ⚡", show_alert=True
        )

    if mod == 'enable':
        # Enable the chatbot for this chat
        chatbot_data[f"{chat_id}_status"] = "enabled"
        save_data(chatbot_data)
        return await m.edit_text(
            f"⚡ Chatbot successfully enabled 🟢 in {m.chat.title or m.chat.first_name} by {query.from_user.mention}"
        )
    elif mod == 'disable':
        # Disable the chatbot for this chat
        chatbot_data[f"{chat_id}_status"] = "disabled"
        save_data(chatbot_data)
        return await m.edit_text(
            f"⚡ Chatbot successfully disabled 🔴 in {m.chat.title or m.chat.first_name} by {query.from_user.mention}"
        )
    else:
        return await query.answer(
            text='Callback data #404 no mod type 🤔', show_alert=True
            )
