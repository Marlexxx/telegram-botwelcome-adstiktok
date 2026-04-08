import logging
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, ChatJoinRequestHandler, ContextTypes

TOKEN = "8340078525:AAGkUtFHaNcjuUVFT89SQhanc8eoS38mz9Y"
CHANNEL_ID = "-1003793799869"
PHOTO_URL = "https://i.postimg.cc/wBXHRZhc/68.png"
MESSAGE_BIENVENUE = """
Hey !  🍓 
Bienvenue sur mon canal telegram ! 💫

Pour te remercier je te partage mon insta privé que j'utilise tout les jours. C'est vraiment pour les intimes ahah 

Envoie moi un message sur telegram pour me dire que tu t'es abonné et je t'enverrais une surprise 💗

https://www.instagram.com/lunarssu7/

A tout de suite !
"""

logging.basicConfig(level=logging.INFO)

async def handle_join_request(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user = update.chat_join_request.from_user
    invite = update.chat_join_request.invite_link
    source = invite.name if invite and invite.name else "inconnu"

    print(f"📊 TRACKING — {datetime.now().strftime('%Y-%m-%d %H:%M')} | {user.first_name} (@{user.username}) | ID: {user.id} | SOURCE: {source}")

    try:
        await ctx.bot.send_photo(
            chat_id=user.id,
            photo=PHOTO_URL,
            caption=MESSAGE_BIENVENUE
        )
        print(f"✅ DM envoyé à {user.first_name}")
    except Exception as e:
        print(f"❌ Impossible d'envoyer à {user.first_name} : {e}")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(ChatJoinRequestHandler(handle_join_request))
    print("🤖 Bot démarré...")
    app.run_polling(allowed_updates=["chat_join_request"])

if __name__ == "__main__":
    main()
