import sqlite3
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from config import OWNER_ID, OWNER_USERNAME

def register_admin_handlers(application):
    application.add_handler(CommandHandler("admin", admin_menu))
    application.add_handler(CommandHandler("users", show_users))
    application.add_handler(CommandHandler("broadcast", broadcast_message))
    application.add_handler(CommandHandler("premium_list", premium_list))
    application.add_handler(CommandHandler("stats", show_stats))

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

async def broadcast_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if str(user_id) != OWNER_ID and update.effective_user.username != OWNER_USERNAME:
        await update.message.reply_text("Anda bukan admin!")
        return
    
    if not context.args:
        await update.message.reply_text("Masukkan pesan yang ingin disiarkan. Contoh: /broadcast Halo semua!")
        return
    
    message = " ".join(context.args)
    
    try:
        conn = sqlite3.connect('suntbot.db')
        c = conn.cursor()
        
        c.execute("SELECT user_id FROM users")
        users = c.fetchall()
        conn.close()
        
        success = 0
        failed = 0
        
        for (user_id,) in users:
            try:
                await context.bot.send_message(chat_id=user_id, text=f"📢 BROADCAST:\n\n{message}")
                success += 1
            except:
                failed += 1
        
        await update.message.reply_text(f"Broadcast selesai!\nBerhasil: {success}\nGagal: {failed}")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

# Implement other admin functions similarly...
