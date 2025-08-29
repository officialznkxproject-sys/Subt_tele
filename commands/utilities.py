import requests
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from config import WEATHER_API_KEY, NEWS_API_KEY

def register_utilities_handlers(application):
    application.add_handler(CommandHandler("weather", get_weather))
    application.add_handler(CommandHandler("news", get_news))
    application.add_handler(CommandHandler("currency", convert_currency))
    application.add_handler(CommandHandler("calculator", calculator))
    application.add_handler(CommandHandler("reminder", set_reminder))
    application.add_handler(CommandHandler("timer", set_timer))
    application.add_handler(CommandHandler("stopwatch", stopwatch))
    application.add_handler(CommandHandler("qrcode", generate_qrcode))
    application.add_handler(CommandHandler("notes", manage_notes))
    application.add_handler(CommandHandler("poll", create_poll))

async def get_weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Masukkan nama kota. Contoh: /weather Jakarta")
        return
    
    city = " ".join(context.args)
    
    try:
        if WEATHER_API_KEY:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=id"
            response = requests.get(url)
            data = response.json()
            
            if data["cod"] != 200:
                await update.message.reply_text("Kota tidak ditemukan.")
                return
            
            weather = data["weather"][0]["description"]
            temp = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            wind = data["wind"]["speed"]
            
            text = f"🌤️ CUACA DI {city.upper()}\n\n"
            text += f"Kondisi: {weather}\n"
            text += f"Suhu: {temp}°C\n"
            text += f"Kelembaban: {humidity}%\n"
            text += f"Angin: {wind} m/s"
        else:
            text = "Fitur cuaca memerlukan konfigurasi API key."
        
        await update.message.reply_text(text)
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

async def get_news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    topic = " ".join(context.args) if context.args else "general"
    
    try:
        if NEWS_API_KEY:
            url = f"https://newsapi.org/v2/everything?q={topic}&language=id&sortBy=publishedAt&apiKey={NEWS_API_KEY}"
            response = requests.get(url)
            data = response.json()
            
            if data["status"] != "ok" or data["totalResults"] == 0:
                await update.message.reply_text("Tidak ada berita ditemukan.")
                return
            
            articles = data["articles"][:5]  # Get top 5 articles
            text = f"📰 BERITA TERBARU - {topic.upper()}\n\n"
            
            for i, article in enumerate(articles, 1):
                title = article["title"]
                source = article["source"]["name"]
                url = article["url"]
                text += f"{i}. {title}\n   Sumber: {source}\n   {url}\n\n"
        else:
            text = "Fitur berita memerlukan konfigurasi API key."
        
        await update.message.reply_text(text)
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

# Implement other utility functions similarly...
