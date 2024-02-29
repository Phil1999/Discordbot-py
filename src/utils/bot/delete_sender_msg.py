import discord

async def delete_sender_message(ctx):

    try:
        await ctx.message.delete()
    except discord.Forbidden:
        return "I don't have permission to delete messages."
    except discord.HTTPException:
        return "Deleting the message failed"