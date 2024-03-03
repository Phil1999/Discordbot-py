from .commands import general
import discord
from utils.decorators import delete_invoke_message

def setup_bot(bot):
    @bot.command(name='hello')
    @delete_invoke_message
    async def hello(ctx):
        await ctx.send(general.hello())
    
    @bot.command(name='guide')
    @delete_invoke_message
    async def help(ctx):
        await ctx.send(general.help())
    
    @bot.command(name='image')
    @delete_invoke_message
    async def image(ctx):
        embed = await general.send_image_url()
        await ctx.send(embed=embed)
    
    @bot.command(name='mrx')
    @delete_invoke_message
    async def mrx(ctx, *usernames: str):

        print(usernames) 
        result, file = await general.send_character_image_url(usernames)

        if isinstance(result, str):
            await ctx.send(result)
            return
    
        if isinstance(result, discord.Embed):
            # Check if a file was also returned
            if file is not None:
                await ctx.send(file=file, embed=result)  # Send both file and embed
            else:
                await ctx.send(embed=result)  # Send only embed if no file is present
    
