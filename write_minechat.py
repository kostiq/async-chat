import asyncio
import json
import logging
import re

import configargparse

logging.basicConfig(level=logging.DEBUG)


def sanitize(message):
    return re.sub('\\n', '', message)


async def register(nickname, host, port):
    nickname = sanitize(nickname)

    reader, writer = await asyncio.open_connection(host, port)

    server_response = await reader.readline()
    logging.debug(f'Received: {server_response.decode()!r}')

    writer.write('\n'.encode())
    logging.debug(f"Send '\\n'")

    server_response = await reader.readline()
    logging.debug(f'Received: {server_response.decode()!r}')

    writer.write(f'{nickname}\n'.encode())
    logging.debug(f'Send {nickname!r}')

    server_response = await reader.readline()
    logging.debug(f'Received: {server_response.decode()!r}')

    writer.close()

    return json.loads(server_response)['account_hash']


async def authorise(reader, writer, account_hash):
    server_response = await reader.readline()
    logging.debug(f'Received: {server_response.decode()!r}')

    writer.write(f'{account_hash}\n'.encode())
    logging.debug(f'Send {account_hash!r}')

    server_response = await reader.readline()

    if not json.loads(server_response.decode()):
        logging.debug('Неизвестный токен. Проверьте его или зарегистрируйте заново.')
    else:
        logging.debug(f'Received: {server_response.decode()!r}')

    return writer


async def submit_message(writer, message):
    message = sanitize(message)
    writer.write(f'{message}\n\n'.encode())
    logging.debug(f'Send {message!r}')


async def write_to_chat(host, port, token, user, message):
    token = token or await register(user, host, port)

    reader, writer = await asyncio.open_connection(host, port)

    writer = await authorise(reader, writer, token)

    await submit_message(writer, message)

    writer.close()


def get_env_params():
    parser = configargparse.ArgParser(default_config_files=['./writer_config.conf'])
    parser.add_argument('--host', env_var='HOST')
    parser.add_argument('--port', env_var='PORT')
    parser.add_argument('--token', env_var='TOKEN')
    parser.add_argument('--username', env_var='USERNAME')
    parser.add_argument('--message', env_var='MESSAGE')

    args = parser.parse_args()

    return args.host, args.port, args.token, args.username, args.message


if __name__ == '__main__':
    asyncio.run(write_to_chat(*get_env_params()))
