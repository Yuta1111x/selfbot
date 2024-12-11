from flask import Flask, send_file
import discord
import asyncio
import os

# Flask Web Server
app = Flask(__name__)
port = 3000

def start_web_server():
    @app.route('/')
    def index():
        return send_file('index.html')

    app.run(host='0.0.0.0', port=port)

# Discord Bot
client = discord.Client(intents=discord.Intents.default(), self_bot=True)
token = os.getenv("TOKEN")

@client.event
async def on_ready():
    print(f"Zalogowano jako: {client.user}")

@client.event
async def on_message(message):
    if message.author != client.user:
        return

    if message.content.lower() == ".ping":
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
                        if deleted >= num:
                            break
                        await asyncio.sleep(1)
                print(f"Usunięto {deleted} wiadomości.") if isinstance(message.channel, discord.DMChannel) else print(f"Usunięto {deleted}.")
            else:
                print("Podaj liczbę większą niż 0.")
        except:
            print("Proszę podać poprawną liczbę.")

    elif message.content.startswith(".anim"):
        text = message.content[6:]
        if text:
            await message.delete()
            lines = text.split('\n')  # Podział na linie
            max_len = max(len(line) for line in lines)
            masked_lines = ['-' * max_len for _ in lines]  # Maskowanie na podstawie najdłuższej linii
            msg = await message.channel.send('\n'.join(masked_lines))
            for i in range(max_len):
                updated_lines = []
                for line in lines:
                    if i < len(line):
                        updated_line = line[:i + 1].ljust(max_len, '-')  # Odkrywamy litery
                    else:
                        updated_line = line.ljust(max_len, '-')  # Zachowujemy odkryte linie
                    updated_lines.append(updated_line)
                await msg.edit(content='\n'.join(updated_lines))
                await asyncio.sleep(0.5)
            await msg.edit(content='\n'.join(lines))  # Ustawienie pełnego tekstu po animacji

# Start both the web server and the Discord bot
if __name__ == "__main__":
    from threading import Thread

    web_thread = Thread(target=start_web_server)
    web_thread.start()

    client.run(token, bot=False)