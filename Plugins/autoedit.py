import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import asyncio, io
from pyrogram import filters
from bot import autocaption
from config import Config
from database.database import *
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait
from music_tag import load_file
from PIL import Image

@autocaption.on_message(filters.private & filters.audio)
async def tag(bot, m):
    fname = m.audio.file_name
    m = await bot.get_messages(m.chat.id, m.message_id)
    file = await m.download(file_name="temp/file.mp3")
    await m.delete()
    music = load_file("temp/file.mp3")
    t = f"{music['title']}"
    a = f"{music['artist']}"
    al = f"{music['album']}"
    g = f"{music['genre']}"
    c = f"{music['comment']}"
    l = f"{music['lyrics']}"
    ar = music['artwork']
    image_data = ar.value.data
    img = Image.open(io.BytesIO(image_data))
    img.save("artwork.jpg")
  
    if fname.split(' ')[0].__contains__("@") or fname.split(' ')[0].__contains__(".me/"):
        fname = fname.split(f"{fname.split(' ')[0]}")[+1]
    elif (fname.__contains__("@") or fname.__contains__(".me/")) and ((not fname.split(' ')[0].__contains__("@")) and (not fname.split(' ')[0].__contains__(".me/"))):
        fname = fname.split(f"{fname.rsplit(' ', 1)[1]}")[0]

    if a.split(' ')[0].__contains__("@") or a.split(' ')[0].__contains__(".me/"):
        a = a.split(f"{a.split(' ')[0]}")[+1]
    elif (a.__contains__("@") or a.__contains__(".me/")) and ((not a.split(' ')[0].__contains__("@")) and (not a.split(' ')[0].__contains__(".me/"))):
        a = a.split(f"{a.rsplit(' ', 1)[1]}")[0]
     
    if al.split(' ')[0].__contains__("@") or al.split(' ')[0].__contains__(".me/"):
        al = al.split(f"{al.split(' ')[0]}")[+1]
    elif (al.__contains__("@") or al.__contains__(".me/")) and ((not al.split(' ')[0].__contains__("@")) and (not al.split(' ')[0].__contains__(".me/"))):
        al = al.split(f"{al.rsplit(' ', 1)[1]}")[0]

    if c.split(' ')[0].__contains__("@") or c.split(' ')[0].__contains__(".me/"):
        c = c.split(f"{c.split(' ')[0]}")[+1]
    elif (c.__contains__("@") or c.__contains__(".me/")) and ((not c.split(' ')[0].__contains__("@")) and (not c.split(' ')[0].__contains__(".me/"))):
        c = c.split(f"{c.rsplit(' ', 1)[1]}")[0]

    if l.split(' ')[0].__contains__("@") or l.split(' ')[0].__contains__(".me/"):
        l = l.split(f"{l.split(' ')[0]}")[+1]
    elif (l.__contains__("@") or l.__contains__(".me/")) and ((not l.split(' ')[0].__contains__("@")) and (not l.split(' ')[0].__contains__(".me/"))):
        l = l.split(f"{l.rsplit(' ', 1)[1]}")[0]

    if t.split(' ')[0].__contains__("@") or t.split(' ')[0].__contains__(".me/"):
        t = t.split(f"{t.split(' ')[0]}")[+1]
    elif (t.__contains__("@") or t.__contains__(".me/")) and ((not t.split(' ')[0].__contains__("@")) and (not t.split(' ')[0].__contains__(".me/"))):
        t = t.split(f"{t.rsplit(' ', 1)[1]}")[0]

    if g.split(' ')[0].__contains__("@") or g.split(' ')[0].__contains__(".me/"):
        g = g.split(f"{g.split(' ')[0]}")[+1]
    elif (g.__contains__("@") or g.__contains__(".me/")) and ((not g.split(' ')[0].__contains__("@")) and (not g.split(' ')[0].__contains__(".me/"))):
        g = g.split(f"{g.rsplit(' ', 1)[1]}")[0]

    music.remove_tag('comment')
    music.remove_tag('artist')
    music.remove_tag('lyrics')
    music.remove_tag('title')
    music.remove_tag('album')
    music.remove_tag('genre')
    music['artist'] = a + Config.custom_tag
    music['title'] = t + Config.custom_tag
    music['album'] = al + Config.custom_tag
    music['genre'] = g + Config.custom_tag
    music['comment'] = c + Config.custom_tag
    music['lyrics'] = l + Config.custom_tag
    music.save()

    try:
        await bot.send_audio(
            chat_id=m.chat.id,
            file_name=fname + ".mp3",
            caption=caption,
            thumb=open('artwork.jpg', 'rb'),
            audio="temp/file.mp3"
        )
    except Exception as e:
        print(e)
