# -*- coding: utf-8 -*-

from typing import NoReturn
from os.path import abspath, dirname
import discord
import asyncio
from discord.ext import commands
from discord.ext.commands import Bot, Context
from discord_slash import cog_ext, SlashContext

from cogs.utils import Config, Logger, Strings, Utils,Settings


CONFIG = Config()
STRINGS = Strings(CONFIG['default_locale'])


class Admin(commands.Cog, name='Admin'):
    """A module required to administer the bot. Only works for its owners."""

    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.name = 'Admin'

    @commands.command()
    @commands.is_owner()
    async def load(self, ctx: Context, *, module: str) -> NoReturn:
        """Loads a module (cog). If the module is not found
            or an error is found in its code, it will throw an error.

        Attributes:
        -----------
        - `module` - the module to load

        """
        try:
            self.bot.load_extension(f'cogs.{module}')
        except Exception as e:
            await ctx.message.add_reaction(CONFIG['no_emoji'])
            embed = Utils.error_embed('`{}`: {}'.format(type(e).__name__, e))
            await ctx.send(embed=embed)
        else:
            await ctx.message.add_reaction(CONFIG['yes_emoji'])

    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx: Context, *, module: str) -> NoReturn:
        """Unloads a module (cog). If the module is not found, it will throw an error.

        Attributes:
        -----------
        - `module` - the module to load

        """
        try:
            self.bot.unload_extension(f'cogs.{module}')
        except Exception as e:
            await ctx.message.add_reaction(CONFIG['no_emoji'])
            embed = Utils.error_embed('`{}`: {}'.format(type(e).__name__, e))
            await ctx.send(embed=embed)
        else:

            await ctx.message.add_reaction(CONFIG['yes_emoji'])

    @commands.command(name='reload')
    @commands.is_owner()
    async def _reload(self, ctx: Context, *, module: str) -> NoReturn:
        """Loads a module (cog). If the module is not found
            or an error is found in its code, it will throw an error.

        Attributes:
        -----------
        - `module` - the module to load

        """
        try:
            self.bot.reload_extension(f'cogs.{module}')
        except Exception as e:
            await ctx.message.add_reaction(CONFIG['no_emoji'])
            embed = Utils.error_embed('`{}`: {}'.format(type(e).__name__, e))
            await ctx.send(embed=embed)
        else:
            await ctx.message.add_reaction(CONFIG['yes_emoji'])

    @commands.command(description='Bot restart/shutdown')
    async def shutdown(self, ctx: SlashContext):  # Команда для выключения бота
        s = await Settings(ctx.guild.id)
        lang = await s.get_field('locale', CONFIG['default_locale'])
        STRINGS = Strings(lang)
        author = ctx.message.author
        valid_users = ["540142383270985738", "573123021598883850", "584377789969596416", "106451437839499264",
                       "237984877604110336", "579750505736044574", "497406228364787717"]
        if str(author.id) in valid_users:
            embed = discord.Embed(title=STRINGS['moderation']['shutdownembedtitle'], description=STRINGS['moderation']['shutdownembeddesc'], color=0xff8000)
            embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar_url)
            await ctx.send(embed=embed)
            await ctx.bot.change_presence(activity=discord.Game(name="Shutting down for either reboot or update "))
            await asyncio.sleep(5)
            print("---------------------------")
            print("[SHUTDOWN] Shutdown requested by bot owner")
            print("---------------------------")
            await ctx.bot.close()
        else:
            embed2 = discord.Embed(title="🔴 Error", description="You need the ``Bot Owner`` permission to do this.",
                                   color=0xdd2e44, )
            await ctx.send(embed=embed2)

    @commands.command(description='Set bot status')
    async def set_status(self, ctx, *args):
        s = await Settings(ctx.guild.id)
        lang = await s.get_field('locale', CONFIG['default_locale'])
        STRINGS = Strings(lang)
        author = ctx.message.author
        valid_users = ["540142383270985738", "573123021598883850", "584377789969596416", "106451437839499264",
                       "237984877604110336", "579750505736044574", "497406228364787717"]
        if str(author.id) in valid_users:
            await self.bot.change_presence(activity=discord.Game(" ".join(args)))
            embed=discord.Embed(title=STRINGS['moderation']['setstatustext'], description=STRINGS['moderation']['setstatusdesc'], color=0xff8000)
            embed.add_field(name=STRINGS['moderation']['setstatusfieldtext'], value=STRINGS['moderation']['setstatusfielddesc'], inline=True)
            embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar_url)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="You failed", description="Need Permission : Bot Owner", color=0xff0000)
            await ctx.send(embed=embed)

    @commands.command(description='Bot invite links')
    async def invite(self, ctx: SlashContext):
        s = await Settings(ctx.guild.id)
        lang = await s.get_field('locale', CONFIG['default_locale'])
        STRINGS = Strings(lang)
        embed = discord.Embed(title=STRINGS['general']['botinvitetitle'], colour=discord.Colour(0xff6900),url="https://discord.com/api/oauth2/authorize?client_id=666304823934844938&permissions=204859462&scope=applications.commands%20bot",description=STRINGS['general']['botinvitedesc'])
        embed.set_author(name=STRINGS['general']['botinvitedescd'],url="https://discord.com/oauth2/authorize?client_id=666304823934844938&scope=bot&permissions=204557314")
        embed.add_field(name=STRINGS['general']['canaryver'], value="https://discord.com/oauth2/authorize?client_id=671612079106424862&scope=bot&permissions=204557314",inline=False)
        embed.add_field(name=STRINGS['general']['botupsdc'], value="https://bots.server-discord.com/666304823934844938",inline=True)
        embed.add_field(name=STRINGS['general']['botuptopgg'], value="https://top.gg/bot/666304823934844938",inline=True)
        embed.add_field(name=STRINGS['general']['botupbod'], value="https://bots.ondiscord.xyz/bots/666304823934844938",inline=True)
        embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        await ctx.send(embed=embed)

    #@commands.command()
    #@commands.is_owner()
    #async def guildlist(self, ctx: SlashContext, bot : Bot):
        #await ctx.send(bot.guilds)


def setup(bot: Bot) -> NoReturn:
    bot.add_cog(Admin(bot))
    Logger.cog_loaded(bot.get_cog('Admin').name)
