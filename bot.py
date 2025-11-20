import discord
from discord.ext import commands
import asyncio
import os
from flask import Flask
from threading import Thread

# =======================
# Flask (pour garder le bot en ligne)
# =======================
app = Flask('')

@app.route('/')
def home():
    return "Bot actif !"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# =======================
# Configuration
# =======================
# Récupération du token depuis les variables d'environnement
try:
    TOKEN = os.environ["TOKEN"]
except KeyError:
    print("ERREUR: La variable d'environnement 'TOKEN' n'est pas définie.")
    exit()

CONFIG_DEPLACEMENT = {
    1440038487503147129: 1439648870740131950,
    1440041307279200377: 1439648870740131950,
    1440042361341214910: 1439648870740131950,
    1440042984706936982: 1439648870740131950,
}

# =======================
# Bot
# =======================
intents = discord.Intents.default()
intents.members = True      # IMPORTANT: Cocher "Server Members Intent" sur le site Discord
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Bot prêt et connecté en tant que : {bot.user}')

@bot.event
async def on_voice_state_update(member, before, after):
    # Si l'utilisateur n'a pas rejoint de salon, on ne fait rien
    if after.channel is None:
        return

    # On vérifie si l'ID du salon rejoint est dans notre liste de règles
    if after.channel.id in CONFIG_DEPLACEMENT:
        
        # On récupère l'ID de destination associé
        destination_id = CONFIG_DEPLACEMENT[after.channel.id]
        salon_arrivee = bot.get_channel(destination_id)
        
        if salon_arrivee:
            try:
                # On déplace le membre
                await member.move_to(salon_arrivee)
                print(f"✅ {member.name} déplacé vers {salon_arrivee.name}")
            except discord.errors.Forbidden:
                print(f"❌ ERREUR : Pas la permission de déplacer {member.name}.")
            except Exception as e:
                print(f"⚠️ Erreur imprévue : {e}")
        else:
            print(f"❌ Erreur : Le salon de destination (ID: {destination_id}) est introuvable.")

# Lancement du serveur Web + Bot
keep_alive()
bot.run(TOKEN)
