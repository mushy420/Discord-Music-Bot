# Discord Music Video Bot

This Discord bot generates random music videos from YouTube and plays them in voice chat when you use the `!music` command.

## Setup

1. Clone this repository.
2. Install the required packages:
3. Install FFmpeg on your system (required for audio playback).
4. Create a `.env` file in the same directory as `bot.py` with the following content: DISCORD_TOKEN=your_discord_bot_token
5. Replace `your_discord_bot_token` with your Discord bot token.
6. Run the bot: python.py

   
## Usage

- `!music` (aliases: `!play`, `!song`, `!start`): Generates a random music video from YouTube and plays it in voice chat.
- `!stop` (alias: `!fuckoff`): Stops the music and disconnects the bot from voice chat.
- `!help`: Shows the list of available commands.

## Features

- Plays music in voice chat using yt-dlp for improved YouTube compatibility
- Rate limiting and cooldowns to prevent spam
- Emoji responses for a more engaging experience
- Robust error handling for various scenarios
- Automatic voice channel management

## Customization

You can customize the bot by modifying the following variables at the top of `bot.py`:

- `PREFIX`: Change the command prefix (default is '!').
- `YOUTUBE_SEARCH_QUERY`: Modify the search query for music videos.

## Note

- Make sure to keep your Discord bot token confidential. Do not share it or commit it to version control systems.
- This bot requires FFmpeg to be installed on your system for audio playback.
- The bot uses the `yt-dlp` library, which is more regularly updated than `youtube-dl` for better compatibility with YouTube's systems.

## Troubleshooting

If you encounter any issues:
1. Ensure FFmpeg is correctly installed and accessible in your system's PATH.
2. Check that all required packages are installed and up to date.
3. Verify that your Discord bot token is correct in the `.env` file.
4. Check the console output for any error messages that may provide more information.

## Best Practices

- The bot includes rate limiting and cooldowns to prevent abuse.
- Error handling is implemented for various scenarios, including command errors, playback issues, and network problems.
- The code is structured for readability and maintainability.
- Comments are included to explain key functionalities.
- The bot uses yt-dlp for improved compatibility and performance with YouTube.

Enjoy your music bot! 🎵🤖
