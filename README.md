# GTA 6 Countdown Discord Bot

A Discord bot with slash commands for the GTA 6 release countdown.

## Features

- `/countdown` shows the remaining time.
- `/release` shows the release date in Discord's local-time format.
- `/setchannel` enables an hourly update in the current text channel.
- `/status` shows bot status and the configured release date.

The default release date is **November 19, 2026 at 00:00 UTC**. Override it with `GTA6_RELEASE_DATE` using an ISO 8601 timestamp.

## Setup

1. Create an application and bot at the [Discord Developer Portal](https://discord.com/developers/applications).
2. Reset and copy the bot token. Never commit it.
3. Use the OAuth2 URL Generator with the `bot` and `applications.commands` scopes. Grant Send Messages, Embed Links, and View Channels.
4. Copy `.env.example` to `.env` and set `DISCORD_TOKEN`.
5. Install dependencies and run:

   ```text
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   python bot.py
   ```

No privileged intents are required. Keep the bot process running for scheduled updates. For hosting, use any Python service that supports long-running workers and environment variables.

## Tests

```text
pip install pytest
pytest
```
