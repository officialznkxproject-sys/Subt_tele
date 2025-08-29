from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

def register_entertainment_handlers(application):
    # Add entertainment command handlers here
    application.add_handler(CommandHandler("joke", tell_joke))
    application.add_handler(CommandHandler("fact", random_fact))
    application.add_handler(CommandHandler("quote", random_quote))
    application.add_handler(CommandHandler("meme", random_meme))

async def tell_joke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    jokes = [
        "Mengapa komputer tidak bisa dingin? Karena ada Windows!",
        "Apa yang dilakukan programmer ketika panas? Mereka buka Windows!",
        "Kenapa programmer tidak bisa berenang? Karena mereka terus sink!",
        "Apa bedanya programmer dan politikus? Programmer hanya buat bug, politikus buat janji bug!",
    ]
    import random
    joke = random.choice(jokes)
    await update.message.reply_text(joke)

async def random_fact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    facts = [
        "Tahukah kamu? Lebah bisa mengenali wajah manusia!",
        "Tahukah kamu? Panda menghabiskan 12 jam sehari untuk makan!",
        "Tahukah kamu? Air laut mengandung sekitar 35 gram garam per liter!",
        "Tahukah kamu? Otak manusia terdiri dari sekitar 75% air!",
    ]
    import random
    fact = random.choice(facts)
    await update.message.reply_text(fact)

async def random_quote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    quotes = [
        "Hidup adalah tentang belajar, jika kamu berhenti belajar, kamu berhenti hidup.",
        "Kesuksesan bukanlah kunci kebahagiaan. Kebahagiaan adalah kunci kesuksesan.",
        "Jangan menunggu kesempatan, ciptakan kesempatan.",
        "Kegagalan adalah kesempatan untuk mulai lagi dengan lebih cerdas.",
    ]
    import random
    quote = random.choice(quotes)
    await update.message.reply_text(quote)

async def random_meme(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Fitur meme sedang dalam pengembangan. Gunakan /joke untuk sekarang!")
