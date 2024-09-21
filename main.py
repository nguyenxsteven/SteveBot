import discord
from discord.ext import commands
import yt_dlp
import os

# Intents (allow the bot to read messages)
intents = discord.Intents.default()
intents.message_content = True

# Bot prefix
bot = commands.Bot(command_prefix="/", intents=intents)

# Download options for youtube-dl/yt-dlp
ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': 'downloads/%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  # Bind to IPv4 since IPv6 addresses cause issues sometimes
}

# Create youtube_dl object with these options
ytdl = yt_dlp.YoutubeDL(ytdl_format_options)

# Bot event when ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# Command to join voice channel
@bot.command(name="join")
async def join(ctx):
    if not ctx.author.voice:
        await ctx.send("You need to be in a voice channel to use this command.")
        return
    channel = ctx.author.voice.channel
    await channel.connect()

# Command to play a song from YouTube
@bot.command(name="play")
async def play(ctx, *, search: str):
    # Ensure the bot is in a voice channel
    if not ctx.voice_client:
        await ctx.author.voice.channel.connect()

    # Search on YouTube for the provided song or URL
    try:
        info = ytdl.extract_info(f"ytsearch:{search}", download=False)  # Search for the song
        if 'entries' in info:
            video = info['entries'][0]  # Get the first result from the search
        else:
            video = info
        url2 = video['url']

        # Specify the FFmpeg path explicitly
        ffmpeg_path = "/nix/store/ffmpeg/bin/ffmpeg"

        # Play the audio
        
        await ctx.send(f"Now playing: {video['title']}")
    except Exception as e:
        await ctx.send("Error occurred while processing the song request.")
        print(e)



# Command to stop the song
@bot.command(name="stop")
async def stop(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()

# Command to leave voice channel
@bot.command(name="leave")
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()

# Run the bot
bot.run(os.getenv("DISCORD_TOKEN"))
