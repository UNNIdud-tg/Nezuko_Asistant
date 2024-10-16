 import unni
import random
from pyrogram import Client as app, filters, errors
from datetime import datetime

# AFK status tracker
AFK = {'afk': False, 'reason': None, 'datetime': None}

# Messages for going AFK and returning
say_afk = [
    'Bye Bye. {}.',
    'Okay {} take some rest.',
    'Nice take care {}',
    'Take your time {}'
]

say_welcome = [
    'Hey {} is Back!',
    'Whats up {}!, are you done?',
    '{} is back online',
    'yeahh {} has returned!'
]

# Function to get current datetime
def get_datetime():
    now = datetime.now()
    return {'date': now.strftime("%Y-%m-%d"), 'time': now.strftime("%H:%M:%S")}

# Function to get an anime gif (placeholder function, implement according to your needs)
async def get_anime_gif(key):
    # Example gif URL, replace this with actual logic
    return "https://example.com/sample_gif.gif"

# Client instance of the bot (replace 'your_bot' with your actual app name)
app = Client('your_bot')

@app.on_message(filters.me, group=2)
async def back_to_online(_, message):
    global AFK
    if AFK['afk']:
        AFK['afk'] = False
        name = message.from_user.mention
        await message.reply(random.choice(say_welcome).format(name))

@app.on_message(filters.me & filters.command('afk', prefixes=unni.PREFIXES), group=1)
async def away_from_keyboard(_, message):
    global AFK

    if len(message.command) < 2:
        reason = None
    else:
        reason = message.text.split(None, 1)[1]

    datetime_info = get_datetime()
    AFK['afk'] = True
    AFK['datetime'] = datetime_info['date'] + ' ' + datetime_info['time']
    AFK['reason'] = reason
    mention = message.from_user.mention

    await message.reply(random.choice(say_afk).format(mention))

@app.on_message(filters.reply & ~filters.me & ~filters.bot, group=-1)
async def afk_check(_, message):
    r = message.reply_to_message
    IS_AFK = AFK['afk']

    if r and IS_AFK and r.from_user.id == unni.OWNER_ID:
        reason = AFK['reason']
        name = message.from_user.mention
        text = f'{name}, My master is offline.\n'
        datetime = AFK['datetime']
        if reason:
            text += f'\nReason: {reason}'
        if datetime:
            text += f'\nSince: {datetime}'
        url = await get_anime_gif("anime_gif_key")
        await message.reply_animation(animation=url, caption=text, quote=True)
