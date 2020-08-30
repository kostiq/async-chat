import asyncio
from datetime import datetime

import aiofiles
import configargparse


async def dump_chat(host, port, log_filename, message_count):
    reader, writer = await asyncio.open_connection(host, port)

    async with aiofiles.open(log_filename, 'w+') as f:
        for _ in range(message_count):
            data = await reader.readline()
            await f.write(f'[{datetime.now().strftime("%d.%m.%Y %H:%M")}] {data.decode()}')


def get_env_params():
    parser = configargparse.ArgParser(default_config_files=['./listen_config.conf'])
    parser.add_argument('--host', env_var='HOST')
    parser.add_argument('--port', env_var='PORT')
    parser.add_argument('--history', env_var='HISTORY_FILENAME')
    parser.add_argument('--message_count', env_var='MESSAGE_COUNT', default=10)

    args = parser.parse_args()

    return args.host, args.port, args.history, args.message_count


if __name__ == '__main__':
    asyncio.run(dump_chat(*get_env_params()))
