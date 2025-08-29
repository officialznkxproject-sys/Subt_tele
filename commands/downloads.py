import yt_dlp
import requests
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

def register_download_handlers(application):
    application.add_handler(CommandHandler("download", download_menu))
    application.add_handler(CommandHandler("ytmp3", youtube_mp3))
    application.add_handler(CommandHandler("ytmp4", youtube_mp4))
    application.add_handler(CommandHandler("tiktok", tiktok_download))
    application.add_handler(CommandHandler("twitter", twitter_download))
    application.add_handler(CommandHandler("facebook", facebook_download))
    application.add_handler(CommandHandler("instagram", instagram_download))

async def download_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """
📥 MENU DOWNLOADER

Pilih platform yang ingin didownload:

1. /ytmp3 [url] - Download YouTube sebagai MP3
2. /ytmp4 [url] - Download YouTube sebagai MP4
3. /tiktok [url] - Download video TikTok
4. /twitter [url] - Download video Twitter
5. /facebook [url] - Download video Facebook
6. /instagram [url] - Download foto/video Instagram

Contoh: /ytmp3 https://www.youtube.com/watch?v=xxxxx
    """
    await update.message.reply_text(text)

async def youtube_mp3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Masukkan URL YouTube. Contoh: /ytmp3 https://www.youtube.com/watch?v=xxxxx")
        return
    
    url = context.args[0]
    await update.message.reply_text("Mengunduh audio... Silakan tunggu.")
    
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': 'downloads/%(title)s.%(ext)s',
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info).replace('.webm', '.mp3').replace('.m4a', '.mp3')
        
        await update.message.reply_audio(audio=open(filename, 'rb'))
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

async def youtube_mp4(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Masukkan URL YouTube. Contoh: /ytmp4 https://www.youtube.com/watch?v=xxxxx")
        return
    
    url = context.args[0]
    await update.message.reply_text("Mengunduh video... Silakan tunggu.")
    
    try:
        ydl_opts = {
            'format': 'best[height<=720]',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
        
        await update.message.reply_video(video=open(filename, 'rb'))
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

# Implement other download functions similarly...
