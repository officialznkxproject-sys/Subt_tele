import logging
import asyncio
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from config import BOT_TOKEN, OWNER_USERNAME, OWNER_ID
from database.models import init_db, add_user, get_user, update_user_premium
from commands.entertainment import register_entertainment_handlers
from commands.utilities import register_utilities_handlers
from commands.downloads import register_download_handlers
from commands.games import register_game_handlers
from commands.ai_features import register_ai_handlers
from commands.admin import register_admin_handlers

# Load environment variables
load_dotenv()
# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize database
init_db()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    username = user.username or user.first_name
    
    # Add user to database
    add_user(user_id, username)
    
    welcome_text = f"""
Halo {user.first_name}! Selamat datang di SUNTbot.

Saya adalah bot dengan 200+ perintah yang dapat membantu Anda dalam berbagai hal.

Fitur yang tersedia:
- Generate foto dan video
- Downloader untuk TikTok, YouTube, Twitter, Facebook, Instagram
- 30+ game seru termasuk RPG
- Fitur AI dengan OpenAI dan Gemini
- Berita dan cuaca terkini
- Dan masih banyak lagi!

Gunakan /help untuk melihat semua perintah yang tersedia.
    """
    
    await update.message.reply_text(welcome_text)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
Daftar Perintah SUNTbot:

🎮 GAMES:
/games - Menu permainan yang tersedia
/rpg - Game RPG
/quiz - Kuis pengetahuan
/tebakgambar - Tebak gambar
/tebakkata - Tebak kata
/susunkata - Susun kata
/catur - Bermain catur
/dam - Bermain dam
/tictactoe - Bermain Tic Tac Toe
/tebakangka - Tebak angka
/tebakbendera - Tebak bendera
/tebaklagu - Tebak lagu
/tebakfilm - Tebak film
/tebakkarakter - Tebak karakter
/memorygame - Game memori
/slotmachine - Mesin slot
/blackjack - Blackjack
/poker - Poker
/tebakkabin - Tebak kabin
/tebakkimia - Tebak unsur kimia
/tebakseleb - Tebak selebriti
/tebaklogo - Tebak logo
/tebakkota - Tebak kota
/tebaknegara - Tebak negara
/tebaktumbuhan - Tebak tumbuhan
/tebakhewan - Tebak hewan
/tebakmerek - Tebak merek
/tebakpepatah - Tebak pepatah
/tebakpantun - Tebak pantun

📥 DOWNLOADER:
/download - Menu downloader
/ytmp3 [url] - Download YouTube sebagai MP3
/ytmp4 [url] - Download YouTube sebagai MP4
/tiktok [url] - Download video TikTok
/twitter [url] - Download video Twitter
/facebook [url] - Download video Facebook
/instagram [url] - Download foto/video Instagram

🎨 GENERATOR:
/generate - Menu generator
/generate_image [prompt] - Generate gambar dari teks
/generate_video [prompt] - Generate video pendek
/generate_music [prompt] - Generate musik
/generate_lyrics [judul] - Generate lirik lagu
/generate_poem - Generate puisi
/generate_story - Generate cerita pendek
/generate_joke - Generate joke
/generate_quote - Generate kutipan
/generate_fact - Generate fakta menarik

🤖 AI FEATURES:
/ai - Menu fitur AI
/ask [pertanyaan] - Tanya ke AI
/translate [teks] - Terjemahkan teks
/summarize [teks] - Ringkas teks
/sentiment [teks] - Analisis sentiment
/grammar [teks] - Perbaiki tata bahasa

🌤️ UTILITIES:
/weather [kota] - Info cuaca
/news [topik] - Berita terkini
/currency [jumlah] [dari] [ke] - Konversi mata uang
/calculator [ekspresi] - Kalkulator
/reminder [waktu] [pesan] - Pengingat
/timer [detik] - Timer
/stopwatch - Stopwatch
/qrcode [teks] - Buat QR code
/notes - Catatan
/poll [pertanyaan] [opsi] - Buat polling

👥 ADMIN:
/admin - Menu admin
/users - Jumlah pengguna
/broadcast [pesan] - Broadcast pesan
/premium_list - Daftar user premium
/stats - Statistik bot

⭐ PREMIUM:
/premium - Info premium
/buy_premium - Beli premium

Gunakan perintah di atas untuk mengakses fitur yang diinginkan.
Untuk informasi lebih lanjut, hubungi @{OWNER_USERNAME}.
    """
    
    await update.message.reply_text(help_text)

async def buy_premium(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = get_user(user_id)
    
    if user and user.get('is_premium', False):
        await update.message.reply_text("Anda sudah menjadi user premium!")
        return
    
    keyboard = [
        [InlineKeyboardButton("Bayar dengan QRIS", callback_data="pay_qris")],
        [InlineKeyboardButton("Konfirmasi Pembayaran", callback_data="confirm_payment")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = """
🛒 BELI PREMIUM

Dapatkan akses ke semua fitur premium dengan membeli paket premium.

Harga: Rp 50,000
Masa aktif: 30 hari

Fitur premium:
- Akses tanpa batas ke semua fitur
- Prioritas dalam antrian
- Fitur generate tanpa batas
- Download tanpa watermark
- Dukungan prioritas

Klik tombol di bawah untuk melakukan pembayaran.
    """
    
    await update.message.reply_text(text, reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    
    if query.data == "pay_qris":
        # Send QRIS image
        await context.bot.send_photo(
            chat_id=query.message.chat_id,
            photo=open("assets/qris.png", "rb"),
            caption="Scan QRIS di atas untuk melakukan pembayaran."
        )
    elif query.data == "confirm_payment":
        # In a real implementation, you would verify payment here
        # For now, we'll just mark as premium
        update_user_premium(user_id, True)
        await query.edit_message_text(
            text="Pembayaran berhasil dikonfirmasi! Sekarang Anda adalah user premium."
        )

def main():
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("buy_premium", buy_premium))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    # Register command handlers from modules
    register_entertainment_handlers(application)
    register_utilities_handlers(application)
    register_download_handlers(application)
    register_game_handlers(application)
    register_ai_handlers(application)
    register_admin_handlers(application)
    
    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    main()
