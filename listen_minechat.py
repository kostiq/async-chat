import asyncio
import logging
from datetime import datetime

import aiofiles
import configargparse

from utils import open_connection


async def dump_chat(host, port, log_filename, message_count):
    logging.debug(f'Run listening with params: {host}, {port}, {log_filename}, {message_count}')
    async with open_connection(host, port) as (reader, writer):
        async with aiofiles.open(log_filename, 'w+') as f:
            while message_count != 0:
                message_count -= 1

                data = await reader.readline()
                message = f'[{datetime.now().strftime("%d.%m.%Y %H:%M")}] {data.decode()}'
                logging.debug(message.strip())
                await f.write(message)


def get_run_params():
    parser = configargparse.ArgParser(default_config_files=['./listen_config.conf'])
    parser.add_argument('--host', env_var='HOST')
    parser.add_argument('--port', env_var='PORT')
    parser.add_argument('--history', env_var='HISTORY_FILENAME')
    parser.add_argument('--message_count', env_var='MESSAGE_COUNT', default=-1)

    args = parser.parse_args()

    return args.host, args.port, args.history, args.message_count


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(dump_chat(*get_run_params()))
