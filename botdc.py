import discord, asyncio, os

client = discord.Client(intents=discord.Intents.default(), self_bot=True)
token = os.getenv("TOKEN")

@client.event
async def on_ready(): print(f"Zalogowano jako: {client.user}")

@client.event
async def on_message(message):
    if message.author != client.user: return
    if message.content.lower() == "ping":
        await message.channel.send(f"Ping: {round(client.latency * 1000)}ms")
    elif message.content.startswith(".clear"):
        try:
            num = int(message.content.split()[1])
            if num > 0:
                deleted = 0
                async for msg in message.channel.history(limit=None):
                    if msg.author.id == client.user.id: 
                        await msg.delete()
                        deleted += 1
                        if deleted >= num: break
                        await asyncio.sleep(1)
                print(f"Usunięto {deleted} wiadomości.") if isinstance(message.channel, discord.DMChannel) else print(f"Usunięto {deleted}.")
            else: await message.channel.send("Podaj liczbę większą niż 0.")
        except: await message.channel.send("Proszę podać poprawną liczbę.")
    elif message.content.startswith(".anim"):
        text = message.content[6:]
        if text: 
            await message.delete()
            msg = await message.channel.send('-' * len(text))
            for i in range(len(text)):
                await msg.edit(content=text[:i + 1].rjust(len(text), '-'))
                await asyncio.sleep(0.2)

client.run(token, bot=False)
