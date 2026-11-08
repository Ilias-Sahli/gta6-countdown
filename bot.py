import asyncio
import os
from datetime import datetime, timezone
from pathlib import Path

import discord
from discord import app_commands
from discord.ext import commands, tasks
from dotenv import load_dotenv

load_dotenv()

DEFAULT_RELEASE_DATE = "2026-11-19T00:00:00+00:00"
CONFIG_FILE = Path("channel.txt")


def parse_release_date(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def release_date() -> datetime:
    return parse_release_date(os.getenv("GTA6_RELEASE_DATE", DEFAULT_RELEASE_DATE))


def countdown_text(now: datetime | None = None) -> str:
    current = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    remaining = release_date() - current
    if remaining.total_seconds() <= 0:
        return "GTA 6 is out now! 🎉"
    days, seconds = remaining.days, remaining.seconds
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    return f"{days} days, {hours} hours, {minutes} minutes, and {seconds} seconds"


def release_text() -> str:
    return f"<t:{int(release_date().timestamp())}:F> (<t:{int(release_date().timestamp())}:R>)"


class CountdownBot(commands.Bot):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self) -> None:
        await self.tree.sync()
        self.update_channel.start()

    async def on_ready(self) -> None:
        print(f"Logged in as {self.user}")

    @tasks.loop(hours=1)
    async def update_channel(self) -> None:
        if not CONFIG_FILE.exists():
            return
        try:
            channel = self.get_channel(int(CONFIG_FILE.read_text().strip()))
            if isinstance(channel, discord.TextChannel):
                await channel.send(f"⏳ GTA 6 countdown: **{countdown_text()}**")
        except (ValueError, discord.DiscordException) as error:
            print(f"Could not update countdown channel: {error}")


bot = CountdownBot()


@bot.tree.command(name="countdown", description="Show the time remaining until GTA 6 releases.")
async def countdown(interaction: discord.Interaction) -> None:
    await interaction.response.send_message(f"⏳ **GTA 6 countdown:** {countdown_text()}")


@bot.tree.command(name="release", description="Show the configured GTA 6 release date.")
async def release(interaction: discord.Interaction) -> None:
    await interaction.response.send_message(f"🎮 **GTA 6 releases:** {release_text()}")


@bot.tree.command(name="status", description="Show the bot status.")
async def status(interaction: discord.Interaction) -> None:
    await interaction.response.send_message(
        f"✅ Online with {len(bot.guilds)} server(s). Release: {release_text()}"
    )


@bot.tree.command(name="setchannel", description="Set this channel for hourly countdown updates.")
@app_commands.default_permissions(manage_guild=True)
async def setchannel(interaction: discord.Interaction) -> None:
    if not interaction.guild or not isinstance(interaction.channel, discord.TextChannel):
        await interaction.response.send_message("This command can only be used in a server text channel.", ephemeral=True)
        return
    if not interaction.user.guild_permissions.manage_guild:
        await interaction.response.send_message("You need Manage Server permission.", ephemeral=True)
        return
    CONFIG_FILE.write_text(str(interaction.channel.id))
    await interaction.response.send_message("✅ Hourly countdown updates are enabled in this channel.")


def main() -> None:
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        raise SystemExit("DISCORD_TOKEN is missing. Copy .env.example to .env and add your bot token.")
    asyncio.run(bot.start(token))


if __name__ == "__main__":
    main()
