from .. import command, module
import asyncio
import telethon as tg

fishing_chat = -1001463155229

class FishingUtils(module.Module):
    name = "Fishing"
    disabled = False
    running = False

    @command.desc("Start fishing!")
    async def cmd_startfish(self, ctx: command.Context):
        self.running = True
        await ctx.respond("`> Fishing started!`")
        while self.running:
            await self.bot.client.send_message(fishing_chat, "/fish@CalsiBot")
            await asyncio.sleep(3)

    @command.desc("Stop fishing!")
    async def cmd_stopfish(self, ctx: command.Context):
        self.running = False
        await ctx.respond("`> Fishing stopped!`")

    async def on_message(self, event: tg.events.NewMessage.Event) -> None:
        if(event.is_group and str(event.chat_id) == str(fishing_chat)):
            await self.bot.client.send_read_acknowledge(event.chat, event.message, clear_mentions = True)
