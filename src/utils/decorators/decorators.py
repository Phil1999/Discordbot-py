from discord.ext import commands
import functools, discord

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

        