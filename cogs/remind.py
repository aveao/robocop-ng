import discord
from datetime import datetime
from discord.ext import commands
from helpers.robocronp import add_job, get_crontab


class Remind:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def remindlist(self, ctx):
        """Lists your reminders."""
        ctab = get_crontab()
        embed = discord.Embed(title=f"Active robocronp jobs")
        for jobtimestamp in ctab["remind"]:
            job_details = ctab["remind"][jobtimestamp][str(ctx.author.id)]
            expiry_timestr = datetime.utcfromtimestamp(int(jobtimestamp))\
                .strftime('%Y-%m-%d %H:%M:%S (UTC)')
            embed.add_field(name=f"Reminder for {expiry_timestr}",
                            value=f"Added on: {job_details['added']}, "
                            f"Text: {job_details['text']}",
                            inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def remind(self, ctx, when: str, *, text: str = "something"):
        """Reminds you about something."""

        expiry_timestamp = self.bot.parse_time(when)
        expiry_datetime = datetime.utcfromtimestamp(expiry_timestamp)
        duration_text = self.bot.get_relative_timestamp(time_to=expiry_datetime,
                                                        include_to=True,
                                                        humanized=True)

        safe_text = self.bot.escape_message(str(text))
        added_on = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S (UTC)")

        add_job("remind",
                ctx.author.id,
                {"text": safe_text, "added": added_on},
                expiry_timestamp)

        await ctx.send(f"{ctx.author.mention}: I'll remind you in DMs about"
                       f" {safe_text} in {duration_text}")


def setup(bot):
    bot.add_cog(Remind(bot))