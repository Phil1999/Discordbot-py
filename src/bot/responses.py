from .commands import general
import discord
from utils.decorators import delete_invoke_message

def setup_bot(bot):
    @bot.command(name='hello')
    async def hello(ctx):
        await ctx.send(general.hello())
    
    @bot.command(name='guide')
    async def help(ctx):
        await ctx.send(general.help())
    
    @bot.command(name='image')
    async def image(ctx):
        embed = await general.send_image_url()
        await ctx.send(embed=embed)
    
    @bot.command(name='mrx')
    async def mrx(ctx, *usernames: str):
        result, file = await general.send_character_image_url(usernames)

        # If the result is a string, it means there was an error or a usage message
        if isinstance(result, str):
            await ctx.send(result)
            return

        # If the result is None, but a file is provided (multiple usernames scenario)
        if result is None and file is not None:
            await ctx.send(file=file)
            return

        # If the result is a discord.Embed, send the embed and optionally a file
        if isinstance(result, discord.Embed):
            # Check if a file was also returned
            if file is not None:
                await ctx.send(file=file, embed=result)  # Send both file and embed
            else:
                await ctx.send(embed=result)  # Send only embed if no file is present    
