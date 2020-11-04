import asyncio
import json
import logging
import re

import configargparse

from utils import open_connection


def sanitize(message):
    return re.sub(r'\n', '', message)


async def register(nickname, host, port):
    nickname = sanitize(nickname)

    async with open_connection(host, port) as (reader, writer):
        server_response = await reader.readline()
        logging.debug(f'Received: {server_response.decode()!r}')

        writer.write('\n'.encode())
        await writer.drain()
        logging.debug(f"Send '\\n'")

        server_response = await reader.readline()
        logging.debug(f'Received: {server_response.decode()!r}')

        writer.write(f'{nickname}\n'.encode())
        await writer.drain()
        logging.debug(f'Send {nickname!r}')

        server_response = await reader.readline()
        logging.debug(f'Received: {server_response.decode()!r}')

        return json.loads(server_response)['account_hash']


async def authorise(reader, writer, account_hash):
    server_response = await reader.readline()
    logging.debug(f'Received: {server_response.decode()!r}')

    writer.write(f'{account_hash}\n'.encode())
    logging.debug(f'Send {account_hash!r}')

    return await reader.readline()


async def submit_message(writer, message):
    message = sanitize(message)
    writer.write(f'{message}\n\n'.encode())
    await writer.drain()
    logging.debug(f'Send {message!r}')


async def write_to_chat(host, port, token, user, message):
    token = token or await register(user, host, port)

    async with open_connection(host, port) as (reader, writer):
        authorise_response = await authorise(reader, writer, token)

        if json.loads(authorise_response.decode()):
            logging.debug(f'Received: {authorise_response.decode()!r}')
            await submit_message(writer, message)
        else:
            logging.debug('Неизвестный токен. Проверьте его или зарегистрируйте заново.')


def get_run_params():
    parser = configargparse.ArgParser(default_config_files=['./writer_config.conf'])
    parser.add_argument('--host', env_var='HOST')
    parser.add_argument('--port', env_var='PORT')
    parser.add_argument('--token', env_var='TOKEN')
    parser.add_argument('--username', env_var='USERNAME')
    parser.add_argument('--message', env_var='MESSAGE')

    args = parser.parse_args()

    return args.host, args.port, args.token, args.username, args.message


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(write_to_chat(*get_run_params()))
