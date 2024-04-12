from discord.ext import commands
import functools, discord
from utils.vars import ADMIN_IDS
from discord import app_commands

def delete_invoke_message(func):
    @functools.wraps(func)

    async def wrapper(ctx, *args, **kwargs):

        try:
            await ctx.message.delete()
        except discord.Forbidden:
            await ctx.send("Deleting the message failed")
            return
        except discord.HTTPException:
            await ctx.send("Deleting the message failed")
            return
        # Continue with the original function
        await func(ctx, *args, **kwargs)
    
    return wrapper


def is_admin():
    async def predicate(interaction: discord.Interaction):
        if interaction.user.id not in ADMIN_IDS:
            await interaction.response.send_message("No permission to run command.", ephemeral=True)
            return False

        return True
    
    return app_commands.check(predicate)

