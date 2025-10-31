import discord
from discord import app_commands
from discord.ext import commands
import os
from keep_alive import keep_alive
from dotenv import load_dotenv
import pathlib

# ===== .env 読み込み =====
env_path = pathlib.Path('.env')
if env_path.exists():
    load_dotenv(env_path)

# ===== Bot設定 =====
TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise ValueError("環境変数 DISCORD_TOKEN が設定されていません")
TOKEN = TOKEN.strip()

GUILD_ID = int(os.getenv("GUILD_ID", "0"))  # テストサーバーID（不要なら0）

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ===== 起動時イベント =====
@bot.event
async def on_ready():
    print(f"✅ ログインしました: {bot.user}")
    await bot.change_presence(activity=discord.Game(name="スラッシュコマンド待機中…"))

# ===== スラッシュコマンド定義 =====
@bot.tree.command(name="hello", description="挨拶するよ！")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"こんにちは、{interaction.user.name}さん！❄")

@bot.tree.command(name="ping", description="Botの応答速度を表示します")
async def ping(interaction: discord.Interaction):
    latency = round(bot.latency * 1000)
    await interaction.response.send_message(f"🏓 Pong! 応答速度: {latency}ms")

# ===== setup_hookでスラッシュコマンド同期 =====
@bot.event
async def setup_hook():
    if GUILD_ID:
        guild = discord.Object(id=GUILD_ID)
        await bot.tree.sync(guild=guild)
        print("🔁 スラッシュコマンド同期完了（ギルド）")
    else:
        await bot.tree.sync()
        print("🌍 グローバルスラッシュコマンド同期完了")

# ===== Render対応 keep_alive =====
keep_alive()

# ===== 実行 =====
bot.run(TOKEN)
