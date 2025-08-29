import openai
import requests
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from config import OPENAI_API_KEY, GEMINI_API_KEY

def register_ai_handlers(application):
    application.add_handler(CommandHandler("ai", ai_menu))
    application.add_handler(CommandHandler("ask", ask_ai))
    application.add_handler(CommandHandler("translate", translate_text))
    application.add_handler(CommandHandler("summarize", summarize_text))
    application.add_handler(CommandHandler("sentiment", analyze_sentiment))
    application.add_handler(CommandHandler("grammar", check_grammar))
    application.add_handler(CommandHandler("generate_image", generate_image))
    application.add_handler(CommandHandler("generate_video", generate_video))
    application.add_handler(CommandHandler("generate_music", generate_music))
    application.add_handler(CommandHandler("generate_lyrics", generate_lyrics))
    application.add_handler(CommandHandler("generate_poem", generate_poem))
    application.add_handler(CommandHandler("generate_story", generate_story))
    application.add_handler(CommandHandler("generate_joke", generate_joke))
    application.add_handler(CommandHandler("generate_quote", generate_quote))
    application.add_handler(CommandHandler("generate_fact", generate_fact))

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
    
    try:
        if OPENAI_API_KEY:
            openai.api_key = OPENAI_API_KEY
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": question}]
            )
            answer = response.choices[0].message.content
        else:
            # Fallback to a simple response if no API key
            answer = f"Saya adalah AI bot. Anda bertanya: {question}\n\nMaaf, fitur AI lengkap memerlukan konfigurasi API key."
        
        await update.message.reply_text(answer)
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

async def generate_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Masukkan prompt. Contoh: /generate_image pemandangan gunung yang indah")
        return
    
    prompt = " ".join(context.args)
    
    try:
        if OPENAI_API_KEY:
            openai.api_key = OPENAI_API_KEY
            response = openai.Image.create(
                prompt=prompt,
                n=1,
                size="512x512"
            )
            image_url = response.data[0].url
            
            # Download and send the image
            image_data = requests.get(image_url).content
            with open("temp_image.png", "wb") as f:
                f.write(image_data)
            
            await update.message.reply_photo(photo=open("temp_image.png", "rb"))
        else:
            await update.message.reply_text("Fitur generate gambar memerlukan konfigurasi API key OpenAI.")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

# Implement other AI functions similarly...
