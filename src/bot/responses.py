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
    async def mrx(ctx, *, username: str = None):
        result = await general.send_character_image_url(username)
        
        if isinstance(result, str):
            await ctx.send(result)
        elif isinstance(result, discord.Embed):
            await ctx.send(embed=result)
        else:
            command_name = ctx.command.name
            await ctx.send(f"Unexpected error occurred when running `{command_name}`.")
    
