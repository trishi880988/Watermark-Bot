import os
import asyncio
from pyrogram import Client, filters
from moviepy.editor import VideoFileClip, CompositeVideoClip, TextClip

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

bot = Client("mybot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@bot.on_message(filters.video & filters.private)
async def add_watermark(client, message):
    await message.reply_text("Downloading video...")
    video = await message.download()
    
    await message.reply_text("Adding watermark...")
    clip = VideoFileClip(video)
    watermark = (TextClip("Join @YourChannel", fontsize=30, color='white', font='Arial-Bold')
                 .set_duration(clip.duration)
                 .set_position(("center", "bottom"))
                 .margin(bottom=20, opacity=0))
    final = CompositeVideoClip([clip, watermark])
    output = "wm_" + os.path.basename(video)
    final.write_videofile(output, codec="libx264", audio_codec="aac")

    await message.reply_video(output, caption="Here is your watermarked video!")
    os.remove(video)
    os.remove(output)

bot.run()
