import logging
import os
import json
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, ChatJoinRequestHandler, ContextTypes
import firebase_admin
from firebase_admin import credentials, firestore

# ─── CONFIG ───────────────────────────────────────────────────────────────────
TOKEN = "8340078525:AAGkUtFHaNcjuUVFT89SQhanc8eoS38mz9Y"
CHANNEL_ID = "-1003793799869"
PHOTO_URL = "https://i.postimg.cc/wBXHRZhc/68.png"
MESSAGE_BIENVENUE = """
Hey !  🍓 
Bienvenue sur mon canal telegram ! 💫

Pour te remercier je te partage mon insta privé que j'utilise tout les jours. C'est vraiment pour les intimes ahah 

Envoie moi un message sur telegram pour me dire que tu t'es abonné et je t'enverrais une surprise 

https://www.instagram.com/lunaxxsd/

A tout de suite !
"""
# ─────────────────────────────────────────────────────────────────────────────

# Init Firebase
cred_json = json.loads(os.environ["FIREBASE_CREDENTIALS"])
cred = credentials.Certificate(cred_json)
firebase_admin.initialize_app(cred)
db = firestore.client()

logging.basicConfig(level=logging.INFO)

async def handle_join_request(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user   = update.chat_join_request.from_user
    invite = update.chat_join_request.invite_link
    source = invite.name if invite and invite.name else "inconnu"

    print(f"📊 TRACKING — {datetime.now().strftime('%Y-%m-%d %H:%M')} | {user.first_name} (@{user.username}) | ID: {user.id} | SOURCE: {source}")

    # Sauvegarde dans Firestore
    db.collection("subscribers").document(str(user.id)).set({
        "user_id":    user.id,
        "first_name": user.first_name,
        "username":   user.username,
        "source":     source,
        "joined_at":  datetime.now().isoformat()
    })

    # ── Incrémente les compteurs sur le compte Instagram correspondant ────────
    try:
        source_lower = source.lower().strip()
        accounts = db.collection("instagram_accounts") \
                     .where("tracking_link", "==", source_lower) \
                     .limit(1) \
                     .stream()

        for acc in accounts:
            acc.reference.update({
                "subs_total": firestore.INCREMENT(1),
                "subs_today": firestore.INCREMENT(1),
            })
            print(f"✅ Compteurs incrémentés pour tracking_link: {source_lower}")
    except Exception as e:
        print(f"⚠️ Erreur increment compteurs: {e}")
    # ─────────────────────────────────────────────────────────────────────────

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
