import discord
from discord.ext import commands
import asyncio
from datetime import datetime, timedelta
import os
from flask import Flask
from threading import Thread

# =======================
# Flask (keepalive)
# =======================
app = Flask('')

@app.route('/')
def home():
    return "Bot actif !"

def run():
    app.run(host='0.0.0.0', port=8080)

Thread(target=run).start()

# =======================
# Bot
# =======================
TOKEN = os.environ["TOKEN"]
CONFIG_DEPLACEMENT = {
    1440038487503147129: 1439648870740131950,
    1440041307279200377: 1439648870740131950,
    1440042361341214910: 1439648870740131950,
    1440042984706936982: 1439648870740131950,
}
# ---------------------

intents = discord.Intents.default()
intents.members = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Bot prêt : {bot.user}')

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
                print(f"Déplacement de {member.name} depuis {after.channel.name} vers {salon_arrivee.name}")
                await member.move_to(salon_arrivee)
            except discord.errors.Forbidden:
                print("ERREUR : Je n'ai pas la permission de déplacer ce membre.")
            except Exception as e:
                print(f"Erreur : {e}")
        else:
            print(f"Erreur : Le salon de destination (ID: {destination_id}) n'existe pas.")

bot.run(TOKEN)