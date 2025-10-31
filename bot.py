import discord
from discord.ext import commands
import os
from keep_alive import keep_alive
from dotenv import load_dotenv  # 追加
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

GUILD_ID = int(os.getenv("GUILD_ID", "1368134670532870194"))

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ===== 起動時イベント =====
@bot.event
async def on_ready():
    print(f"✅ ログインしました: {bot.user}")
    await bot.change_presence(activity=discord.Game(name="スラッシュコマンド待機中…"))

# ===== modules自動ロード =====
async def load_modules():
    for filename in os.listdir("./modules"):
        if filename.endswith(".py") and not filename.startswith("__"):
            module_name = filename[:-3]
            try:
                await bot.load_extension(f"modules.{module_name}")
                print(f"📦 モジュール読み込み: {module_name}")
            except Exception as e:
                print(f"❌ モジュール {module_name} の読み込みに失敗: {e}")

# ===== setup_hookでロード & スラッシュ同期 =====
@bot.event
async def setup_hook():
    await load_modules()
    if GUILD_ID:
        guild = discord.Object(id=GUILD_ID)
        await bot.tree.sync(guild=guild)
        print("🔁 スラッシュコマンド同期完了")

# ===== Render対応 keep_alive =====
keep_alive()

# ===== 実行 =====
bot.run(TOKEN)
