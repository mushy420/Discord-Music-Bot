import os
import random
import asyncio
import discord
from discord.ext import commands
import yt_dlp
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot configuration
TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = '!'

# YouTube search query
YOUTUBE_SEARCH_QUERY = 'music video'

# Set up the bot
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

# yt-dlp configuration
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

ffmpeg_options = {
    'options': '-vn',
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'
}

ytdl = yt_dlp.YoutubeDL(ydl_opts)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=True):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        
        if 'entries' in data:
            data = data['entries'][0]
        
        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command(name='music', aliases=['play', 'song', 'start'], help='Generates a random music video and plays it in voice chat')
@commands.cooldown(1, 10, commands.BucketType.user)
async def music(ctx):
    try:
        # Check if the user is in a voice channel
        if not ctx.author.voice:
            await ctx.send("You need to be in a voice channel to use this command. 🎧")
            return

        # Connect to the voice channel if not already connected
        if not ctx.voice_client:
            await ctx.author.voice.channel.connect()
        elif ctx.voice_client.channel != ctx.author.voice.channel:
            await ctx.voice_client.move_to(ctx.author.voice.channel)

        async with ctx.typing():
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = await asyncio.get_event_loop().run_in_executor(None, lambda: ydl.extract_info(f"ytsearch10:{YOUTUBE_SEARCH_QUERY}", download=False))
                if 'entries' in info and info['entries']:
                    video = random.choice(info['entries'])
                    video_url = video['webpage_url']
                    
                    if ctx.voice_client.is_playing():
                        ctx.voice_client.stop()

                    # Play the audio
                    try:
                        player = await YTDLSource.from_url(video_url, loop=bot.loop, stream=True)
                        ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)
                        await ctx.send(f"🎵 Now playing: {player.title} {video_url}")
                    except Exception as e:
                        await ctx.send(f"An error occurred while trying to play the song: {str(e)} 😔")
                        print(f"Playback error: {e}")
                else:
                    await ctx.send("Sorry, I couldn't find any music videos at the moment. 😕")
    except asyncio.TimeoutError:
        await ctx.send("The operation timed out. Please try again later. ⏳")
    except discord.errors.ClientException as e:
        await ctx.send(f"A Discord client error occurred: {str(e)} 😔")
        print(f"Discord client error: {e}")
    except Exception as e:
        await ctx.send("An unexpected error occurred. Please try again later. 😔")
        print(f"Unexpected error: {e}")

@bot.command(name='stop', aliases=['fuckoff'], help='Stops the music and disconnects the bot from voice')
async def stop(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("Okay, I'm leaving! 👋")
    else:
        await ctx.send("I'm not connected to a voice channel. 🤷‍♂️")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"This command is on cooldown. Please try again in {error.retry_after:.2f} seconds. ⏳")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("Invalid command. Use !help to see available commands. 🤔")
    else:
        print(f"An error occurred: {error}")
        await ctx.send("An error occurred. Please try again later. 😔")

if __name__ == '__main__':
    bot.run(TOKEN)
