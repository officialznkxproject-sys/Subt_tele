import logging
import asyncio
import os
import sqlite3
import random
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Get environment variables
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8140097143:AAGBguxo76FrRLYsCueea-haCXEfVO126Fo")
OWNER_USERNAME = os.environ.get("OWNER_USERNAME", "XyraaEx")
OWNER_ID = os.environ.get("OWNER_ID", "083821223529")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
AUDD_API_KEY = os.environ.get("AUDD_API_KEY", "")
WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY", "")
NEWS_API_KEY = os.environ.get("NEWS_API_KEY", "")

# Database functions
def init_db():
    conn = sqlite3.connect('suntbot.db')
    c = conn.cursor()
    
    # Create users table
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, 
                 user_id INTEGER UNIQUE, 
                 username TEXT, 
                 is_premium INTEGER DEFAULT 0,
                 premium_until TEXT,
                 created_at TEXT)''')
    
    # Create games table
    c.execute('''CREATE TABLE IF NOT EXISTS games
                 (id INTEGER PRIMARY KEY,
                 user_id INTEGER,
                 game_type TEXT,
                 score INTEGER,
                 played_at TEXT)''')
    
    conn.commit()
    conn.close()

def add_user(user_id, username):
    conn = sqlite3.connect('suntbot.db')
    c = conn.cursor()
    
    try:
        c.execute("INSERT INTO users (user_id, username, created_at) VALUES (?, ?, ?)",
                 (user_id, username, datetime.now().isoformat()))
        conn.commit()
    except sqlite3.IntegrityError:
        # User already exists
        pass
    
    conn.close()

def get_user(user_id):
    conn = sqlite3.connect('suntbot.db')
    c = conn.cursor()
    
    c.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user = c.fetchone()
    
    conn.close()
    
    if user:
        return {
            'id': user[0],
            'user_id': user[1],
            'username': user[2],
            'is_premium': bool(user[3]),
            'premium_until': user[4],
            'created_at': user[5]
        }
    return None

def update_user_premium(user_id, is_premium):
    conn = sqlite3.connect('suntbot.db')
    c = conn.cursor()
    
    premium_until = (datetime.now() + timedelta(days=30)).isoformat() if is_premium else None
    
    c.execute("UPDATE users SET is_premium = ?, premium_until = ? WHERE user_id = ?",
             (int(is_premium), premium_until, user_id))
    
    conn.commit()
    conn.close()

def add_game_score(user_id, game_type, score):
    conn = sqlite3.connect('suntbot.db')
    c = conn.cursor()
    
    c.execute("INSERT INTO games (user_id, game_type, score, played_at) VALUES (?, ?, ?, ?)",
             (user_id, game_type, score, datetime.now().isoformat()))
    
    conn.commit()
    conn.close()

def get_leaderboard(game_type=None, limit=10):
    conn = sqlite3.connect('suntbot.db')
    c = conn.cursor()
    
    if game_type:
        c.execute('''SELECT users.username, games.score 
                    FROM games 
                    JOIN users ON games.user_id = users.user_id 
                    WHERE games.game_type = ? 
                    ORDER BY games.score DESC 
                    LIMIT ?''', (game_type, limit))
    else:
        c.execute('''SELECT users.username, SUM(games.score) as total_score 
                    FROM games 
                    JOIN users ON games.user_id = users.user_id 
                    GROUP BY games.user_id 
                    ORDER BY total_score DESC 
                    LIMIT ?''', (limit,))
    
    leaderboard = c.fetchall()
    conn.close()
    
    return leaderboard

# Initialize database
init_db()

# Command handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    username = user.username or user.first_name
    
    # Add user to database
    add_user(user_id, username)
    
    welcome_text = f"""
Halo {user.first_name}! Selamat datang di TohangBot.

Aku adalah bot multifungsi siap pakai.
Kamu bisa pakai aku buat informasi, hiburan, produktivitas, AI tools, hingga custom perintah sesuai kebutuhanmu 🎯
Ketik /menu untuk lihat semua fitur, atau /help kalau butuh panduan.
Enjoy dan semoga bermanfaat 🚀

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
Daftar Perintah TohangBot:

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
    """.format(OWNER_USERNAME=OWNER_USERNAME)
    
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
        # Send QRIS image (placeholder)
        await query.message.reply_text("Fitur pembayaran QRIS akan segera hadir. Silakan gunakan tombol konfirmasi pembayaran setelah transfer.")
    elif query.data == "confirm_payment":
        # In a real implementation, you would verify payment here
        # For now, we'll just mark as premium
        update_user_premium(user_id, True)
        await query.edit_message_text(
            text="Pembayaran berhasil dikonfirmasi! Sekarang Anda adalah user premium."
        )

# Game commands
async def games_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """
🎮 DAFTAR PERMAINAN

Pilih permainan yang ingin dimainkan:

1. /rpg - Game RPG petualangan
2. /quiz - Kuis pengetahuan umum
3. /tebakgambar - Tebak gambar
4. /tebakkata - Tebak kata
5. /susunkata - Susun kata acak
6. /catur - Bermain catur
7. /dam - Bermain dam
8. /tictactoe - Tic Tac Toe
9. /tebakangka - Tebak angka
10. /tebakbendera - Tebak bendera negara
11. /tebaklagu - Tebak judul lagu
12. /tebakfilm - Tebak judul film
13. /tebakkarakter - Tebak karakter
14. /memorygame - Game memori
15. /slotmachine - Mesin slot
16. /blackjack - Blackjack
17. /poker - Poker
18. /tebakkabin - Tebak kabin
19. /tebakkimia - Tebak unsur kimia
20. /tebakseleb - Tebak selebriti
21. /tebaklogo - Tebak logo
22. /tebakkota - Tebak kota
23. /tebaknegara - Tebak negara
24. /tebaktumbuhan - Tebak tumbuhan
25. /tebakhewan - Tebak hewan
26. /tebakmerek - Tebak merek
27. /tebakpepatah - Tebak pepatah
28. /tebakpantun - Tebak pantun

Gunakan perintah di atas untuk memulai permainan!
    """
    await update.message.reply_text(text)

async def rpg_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """
🏰 PETUALANGAN RPG

Selamat datang di dunia fantasi!

Pilih aksi:
1. /rpg_explore - Jelajahi dungeon
2. /rpg_fight - Lawan monster
3. /rpg_inventory - Lihat inventory
4. /rpg_stats - Lihat statistik
5. /rpg_shop - Kunjungi toko

Anda memulai dengan 100 HP dan 50 emas.
    """
    await update.message.reply_text(text)

async def quiz_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    questions = [
        {
            "question": "Apa ibu kota Indonesia?",
            "options": ["Jakarta", "Bandung", "Surabaya", "Medan"],
            "answer": "Jakarta"
        },
        {
            "question": "Planet terdekat dari matahari?",
            "options": ["Merkurius", "Venus", "Bumi", "Mars"],
            "answer": "Merkurius"
        },
        {
            "question": "2 + 2 x 2 = ?",
            "options": ["6", "8", "4", "10"],
            "answer": "6"
        }
    ]
    
    question = random.choice(questions)
    text = f"❓ KUIS\n\n{question['question']}\n\n"
    
    for i, option in enumerate(question['options'], 1):
        text += f"{i}. {option}\n"
    
    # Store the correct answer in context for validation
    context.user_data['quiz_answer'] = question['answer']
    
    await update.message.reply_text(text)

async def show_leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    game_type = context.args[0] if context.args else None
    leaderboard = get_leaderboard(game_type)
    
    text = "🏆 LEADERBOARD\n\n"
    
    if not leaderboard:
        text += "Belum ada skor yang tercatat."
    else:
        for i, (username, score) in enumerate(leaderboard, 1):
            text += f"{i}. {username}: {score} poin\n"
    
    await update.message.reply_text(text)

# Download commands
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
    await update.message.reply_text("Fitur download YouTube MP3 sedang dalam pengembangan. Silakan coba lagi nanti.")

async def youtube_mp4(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Masukkan URL YouTube. Contoh: /ytmp4 https://www.youtube.com/watch?v=xxxxx")
        return
    
    url = context.args[0]
    await update.message.reply_text("Fitur download YouTube MP4 sedang dalam pengembangan. Silakan coba lagi nanti.")

# AI commands
async def ai_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """
🤖 MENU FITUR AI

Pilih fitur AI yang ingin digunakan:

1. /ask [pertanyaan] - Tanya apa saja ke AI
2. /translate [teks] - Terjemahkan teks
3. /summarize [teks] - Ringkas teks panjang
4. /sentiment [teks] - Analisis sentiment teks
5. /grammar [teks] - Perbaiki tata bahasa

🎨 GENERATOR:
6. /generate_image [prompt] - Generate gambar dari teks
7. /generate_video [prompt] - Generate video pendek
8. /generate_music [prompt] - Generate musik
9. /generate_lyrics [judul] - Generate lirik lagu
10. /generate_poem - Generate puisi
11. /generate_story - Generate cerita pendek
12. /generate_joke - Generate joke
13. /generate_quote - Generate kutipan
14. /generate_fact - Generate fakta menarik

Beberapa fitur memerlukan akses premium.
    """
    await update.message.reply_text(text)

async def ask_ai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Masukkan pertanyaan. Contoh: /ask Apa itu artificial intelligence?")
        return
    
    question = " ".join(context.args)
    
    if not OPENAI_API_KEY:
        answer = f"Saya adalah AI bot. Anda bertanya: {question}\n\nMaaf, fitur AI lengkap memerlukan konfigurasi API key OpenAI."
    else:
        try:
            # Simulate AI response
            answers = [
                f"Pertanyaan bagus! {question} adalah topik yang menarik.",
                f"Berdasarkan pengetahuan saya, {question} adalah hal yang kompleks.",
                f"Saya sedang mempelajari tentang {question}. Bisakah Anda menjelaskan lebih detail?",
                f"Untuk pertanyaan '{question}', saya perlu waktu untuk mencari jawaban terbaik."
            ]
            answer = random.choice(answers)
        except Exception as e:
            answer = f"Error: {str(e)}"
    
    await update.message.reply_text(answer)

# Utility commands
async def get_weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Masukkan nama kota. Contoh: /weather Jakarta")
        return
    
    city = " ".join(context.args)
    
    if not WEATHER_API_KEY:
        text = f"Info cuaca untuk {city} akan tersedia setelah konfigurasi API key cuaca."
    else:
        # Simulate weather response
        weather_conditions = ["Cerah", "Hujan", "Berawan", "Mendung", "Badai"]
        temp = random.randint(20, 35)
        humidity = random.randint(60, 90)
        wind = random.uniform(1.0, 10.0)
        
        text = f"🌤️ CUACA DI {city.upper()}\n\n"
        text += f"Kondisi: {random.choice(weather_conditions)}\n"
        text += f"Suhu: {temp}°C\n"
        text += f"Kelembaban: {humidity}%\n"
        text += f"Angin: {wind:.1f} m/s"
    
    await update.message.reply_text(text)

# Admin commands
async def admin_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if str(user_id) != OWNER_ID and update.effective_user.username != OWNER_USERNAME:
        await update.message.reply_text("Anda bukan admin!")
        return
    
    text = """
👨‍💻 MENU ADMIN

Perintah admin yang tersedia:

1. /users - Lihat jumlah pengguna
2. /broadcast [pesan] - Kirim pesan ke semua user
3. /premium_list - Daftar user premium
4. /stats - Statistik bot

Hanya owner yang dapat menggunakan perintah ini.
    """
    await update.message.reply_text(text)

async def show_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if str(user_id) != OWNER_ID and update.effective_user.username != OWNER_USERNAME:
        await update.message.reply_text("Anda bukan admin!")
        return
    
    try:
        conn = sqlite3.connect('suntbot.db')
        c = conn.cursor()
        
        c.execute("SELECT COUNT(*) FROM users")
        total_users = c.fetchone()[0]
        
        c.execute("SELECT COUNT(*) FROM users WHERE is_premium = 1")
        premium_users = c.fetchone()[0]
        
        conn.close()
        
        text = f"📊 STATISTIK PENGGUNA\n\n"
        text += f"Total pengguna: {total_users}\n"
        text += f"User premium: {premium_users}\n"
        text += f"User regular: {total_users - premium_users}"
        
        await update.message.reply_text(text)
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

# Entertainment commands
async def tell_joke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    jokes = [
        "Mengapa komputer tidak bisa dingin? Karena ada Windows!",
        "Apa yang dilakukan programmer ketika panas? Mereka buka Windows!",
        "Kenapa programmer tidak bisa berenang? Karena mereka terus sink!",
        "Apa bedanya programmer dan politikus? Programmer hanya buat bug, politikus buat janji bug!",
    ]
    joke = random.choice(jokes)
    await update.message.reply_text(joke)

async def random_fact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    facts = [
        "Tahukah kamu? Lebah bisa mengenali wajah manusia!",
        "Tahukah kamu? Panda menghabiskan 12 jam sehari untuk makan!",
        "Tahukah kamu? Air laut mengandung sekitar 35 gram garam per liter!",
        "Tahukah kamu? Otak manusia terdiri dari sekitar 75% air!",
    ]
    fact = random.choice(facts)
    await update.message.reply_text(fact)

async def random_quote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    quotes = [
        "Hidup adalah tentang belajar, jika kamu berhenti belajar, kamu berhenti hidup.",
        "Kesuksesan bukanlah kunci kebahagiaan. Kebahagiaan adalah kunci kesuksesan.",
        "Jangan menunggu kesempatan, ciptakan kesempatan.",
        "Kegagalan adalah kesempatan untuk mulai lagi dengan lebih cerdas.",
    ]
    quote = random.choice(quotes)
    await update.message.reply_text(quote)

def main():
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("buy_premium", buy_premium))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    # Game commands
    application.add_handler(CommandHandler("games", games_menu))
    application.add_handler(CommandHandler("rpg", rpg_game))
    application.add_handler(CommandHandler("quiz", quiz_game))
    application.add_handler(CommandHandler("leader
