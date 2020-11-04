# async-chat

Репозиторий содержит скрипты для чтения и записи в удаленный чат.

Для работы понадобится виртуальное окружение со всеми зависимостями.

    virtualenv venv --python=python3
    source venv/bin/activate
    pip install -r requirements.txt
  

## Listen minechat

Скрипт для логирования чата в файл. 

    python listen_minechat.py
   
Конфигурирется с помощью `cli` параметров, переменных окружения или `listen_config.config`

Доступные параметры:

`--host` or env var `HOST` - адрес чата.

`--port` or env var `PORT` - порт чата.  

`--history` or env var `HISTORY_FILENAME` - имя файла, куда будет сдамплен чат.

`--message_count` or env var `MESSAGE_COUNT` - количество сдампленных сообщений (по умолчанию 10).

## Write minechat

Скрипт для логирования чата в файл. 

    python write_minechat.py

Конфигурирется с помощью `cli` параметров, переменных окружения или `writer_config.conf`

Доступные параметры:

`--host` or env var `HOST` - адрес чата.

`--port` or env var `PORT` - порт чата.

`--token` or env var `TOKEN` - token пользователя для авторизации в чате.  

`--username` or env var `USERNAME` - если `token` не продоствлен или невалидный, то будет зарегестрирован новый пользователь с данным `username` .

`--message` or env var `MESSAGE` - сообщение, которое будет отправлено в чат.

**Символ переноса строки `\n` в параметрах `username` и `message` будет удален.**
