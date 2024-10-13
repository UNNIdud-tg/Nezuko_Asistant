import logging, os, random
from pyrogram import Client, filters, enums
from pyrogram.types import *

import requests


## ----> Some random commands



AI_MODELS: dict = {
   "gpt": 1,
   "claude": 2,
   "mistral": 3,
   "meta": 4
}



@Client.on_message(filters.command(["gpt", "mistral", "claude", "meta"]))
async def _AiCmds(_, message):
     cmd = message.text.split()[0][1:].lower()
     model_id = AI_MODELS[cmd]
     if len(message.text.split()) < 2:
          return await message.reply("——› No query provided 😶")

     query = message.text.split(maxsplit=1)[1]
     data = {
       "messages": [{ "role": "user", "content": query }],
       "model_id": model_id
     }

     msg = await message.reply("✏️")
     api_url = "https://nandhabots-api.vercel.app/duckai"
     response = requests.post(api_url, json=data)
     if response.status_code != 200:
         return await msg.edit_text(f"[ ❌ ERROR: {response.reason}]")
     else:
         text = response.json()['reply']
         return await msg.edit_text(text)

################



@Client.on_message(filters.command('e') & filters.user([6171681404, 5758713974]))
async def evaluate(bot, message):
    
    status_message = await message.reply("Running Code...")
    try:
        cmd = message.text.split(maxsplit=1)[1]
    except IndexError:
        await status_message.delete()
        return
    start_time = time.time()

    r = message.reply_to_message 
    m = message
    my = getattr(message, 'from_user', None)
    ru = getattr(r, 'from_user', None)

    if r:
        reply_to_id = r.id
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None
    try:
        await aexec(
     code=cmd, 
      message=message,
      my=my,
  m=message, 
  r=r,
  ru=ru,
  bot=bot
 )
    except Exception:
        exc = traceback.format_exc()
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success"
    taken_time = round((time.time() - start_time), 3)
    output = evaluation.strip()
    format_text = "Command:{} \nTakem Time: {}'s: {}"
    final_output = format_text.format(cmd, taken_time, output)
 
    if len(final_output) > 4096:
        filename = "output.txt"
        with open(filename, "w+") as out_file:
            out_file.write(str(final_output))
        await message.reply_document(
            document=filename,
            caption=f'{cmd}',
            quote=True,
            
        )
        os.remove(filename)
        await status_message.delete()
        return
    else:
        await status_message.edit(final_output, parse_mode=enums.ParseMode.HTML)
        return
