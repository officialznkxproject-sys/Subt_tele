import random
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from database.models import add_game_score, get_leaderboard

def register_game_handlers(application):
    application.add_handler(CommandHandler("games", games_menu))
    application.add_handler(CommandHandler("rpg", rpg_game))
    application.add_handler(CommandHandler("quiz", quiz_game))
    application.add_handler(CommandHandler("tebakgambar", tebak_gambar))
    application.add_handler(CommandHandler("tebakkata", tebak_kata))
    application.add_handler(CommandHandler("susunkata", susun_kata))
    application.add_handler(CommandHandler("catur", catur_game))
    application.add_handler(CommandHandler("dam", dam_game))
    application.add_handler(CommandHandler("tictactoe", tictactoe_game))
    application.add_handler(CommandHandler("tebakangka", tebak_angka))
    application.add_handler(CommandHandler("tebakbendera", tebak_bendera))
    application.add_handler(CommandHandler("tebaklagu", tebak_lagu))
    application.add_handler(CommandHandler("tebakfilm", tebak_film))
    application.add_handler(CommandHandler("tebakkarakter", tebak_karakter))
    application.add_handler(CommandHandler("memorygame", memory_game))
    application.add_handler(CommandHandler("slotmachine", slot_machine))
    application.add_handler(CommandHandler("blackjack", blackjack))
    application.add_handler(CommandHandler("poker", poker))
    application.add_handler(CommandHandler("tebakkabin", tebak_kabin))
    application.add_handler(CommandHandler("tebakkimia", tebak_kimia))
    application.add_handler(CommandHandler("tebakseleb", tebak_seleb))
    application.add_handler(CommandHandler("tebaklogo", tebak_logo))
    application.add_handler(CommandHandler("tebakkota", tebak_kota))
    application.add_handler(CommandHandler("tebaknegara", tebak_negara))
    application.add_handler(CommandHandler("tebaktumbuhan", tebak_tumbuhan))
    application.add_handler(CommandHandler("tebakhewan", tebak_hewan))
    application.add_handler(CommandHandler("tebakmerek", tebak_merek))
    application.add_handler(CommandHandler("tebakpepatah", tebak_pepatah))
    application.add_handler(CommandHandler("tebakpantun", tebak_pantun))
    application.add_handler(CommandHandler("leaderboard", show_leaderboard))

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
    # Simple RPG game implementation
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

# Implement other game functions similarly...

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
