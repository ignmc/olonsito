# bot.py
import os
from datetime import datetime

import discord
from dotenv import load_dotenv

from evaluator import write_file_input, delete_file, parse_result, evaluate_case

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()


async def easter(message):

    content = message.content.strip().strip('`').strip()

    if any([
        content.startswith(greeting) for greeting in [
            'hola',
            'oli',
            'holi',
            'ola',
        ]
    ]):
        await message.channel.send("holiwi c:")
        return True

    if content.startswith('uwu'):
        await message.channel.send('uwu~')
        return True

    if content.lower().startswith('aaa'):
        await message.channel.send('Do not despair pls <3')
        return True

    if content == '<3':
        await message.channel.send('<3')
        return True

    if 'callate' in content.lower() or 'cállate' in content.lower():
        await message.channel.send('bueno u.u')
        return True

    return False


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):

    if message.author.bot:
        return

    if not message.guild:

        user_id = str(message.author)
        print(f'Received message from {user_id}')
        content = message.content.strip().strip('`').strip()

        with open('botlog.log', 'a') as log:
            log.write('\n'.join([
                datetime.now().isoformat(),
                f"Message from {user_id}",
                message.content,
                '',
            ]))

        # TODO: validate message? don't hack me pls D:

        if await easter(message):
            return

        subtask, _, code = content.partition('\n')
        try:
            subtask = int(subtask)
        except ValueError:
            await message.channel.send("Mensaje inválido. La primera línea de tu respuesta debe ser un entero "
                                       "que indique la subtarea que intentas resolver (1, 2, o 3) y luego tu "
                                       "solución comenzando en la segunda línea.\n\n"
                                       "Por ejemplo:\n\n"
                                       "```\n"
                                       "2\n"
                                       "repetir:\n"
                                       "  avanzar\n"
                                       "fin repetir;```")
            return

        # Write submission to a temporary file
        file_path = write_file_input(code, user_id)
        # Evaluate solution
        output = evaluate_case(file_path, subtask)
        # Delete temporary file
        delete_file(file_path)

        response_message = parse_result(output)

        with open('botlog.log', 'a') as log:
            log.write('\n'.join([
                f'Response --> {response_message}',
                "------------------------------",
            ]))

        await message.channel.send(response_message)

client.run(TOKEN)
