import argparse
import yaml
from typing import Dict, Union
from exceptions import ConfigMissingFields, ConfigFileDoesNotExist, ConfigException, DialogNotFound
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError, ApiIdInvalidError, PhoneNumberInvalidError
import asyncio
import datetime
import pytz

REQUIRED_CONFIGS = ['api_id', 'api_hash', 'username', 'phone']
DEFAULT_DAYS = [60]


def parse_config(args) -> Union[Dict[str, str], None]:
    """Parse config YAML file"""
    filename = args.config_file[0]
    try:
        with open(filename, 'r') as config_file:
            data = yaml.safe_load(config_file)['data']

            if data is None:  # In case it couldn't parse a YAML config file, or this file doesn't exist
                raise ConfigException
            if not all(x in data for x in REQUIRED_CONFIGS):  # In case required fields in YAML config are missing
                raise ConfigMissingFields

            return data
    except IOError as e:
        raise ConfigFileDoesNotExist
    except Exception:
        raise ConfigException


async def delete_messages(data, chat_name, days):
    """Starts telegram client session and deletes messages from the given chat"""
    # Create the client and connect
    async with TelegramClient(data["username"], data["api_id"], data["api_hash"]) as client:
        await client.start()
        print("Client Created")
        # Ensure you're authorized
        if not await client.is_user_authorized():
            await client.send_code_request(data["phone"])
            try:
                await client.sign_in(data["phone"], input('Enter the code: '))
            except SessionPasswordNeededError:
                await client.sign_in(password=input('Password: '))

        chat = None  # ID of the chat

        async for dialog in client.iter_dialogs():  # Find chat with given name
            if dialog.name == chat_name:
                chat = dialog
                break

        if chat is None:  # If chat was not found
            raise DialogNotFound

        me = await client.get_me()  # Your account

        messages = []

        # Threshold for the messages to be removed
        threshold = datetime.datetime.now().replace(tzinfo=pytz.UTC) - datetime.timedelta(days)

        async for message in client.iter_messages(chat, from_user=me):  # Collect messages by the threshold date
            if message.date > threshold:
                messages.append(message)
            else:
                break

        await client.delete_messages(chat, messages)  # Remove all the collected messages from the chat
        print(f"{len(messages)} was removed from the chat")


async def main():
    parser = argparse.ArgumentParser(description="message remover from telegram chat")

    # Chat name argument
    parser.add_argument("-chn", "--chatname", nargs=1, metavar="chat", type=str, required=True,
                        help="Name of the chat, in which the messages will be removed")

    # Config file argument
    parser.add_argument("-cfg", "--config_file", nargs=1, metavar="config_file", type=str, required=True,
                        help="Config file with: api_id, api_hash, phone, username. Format: .yml, .yaml")

    # From how many days ago start deleting messages
    parser.add_argument('-days', "--days_delete", nargs=1, metavar="days_to_delete", type=int, default=DEFAULT_DAYS,
                        help="From how many days ago start deleting messages. Default: 60 days")

    args = parser.parse_args()  # Parse arguments of cli

    try:
        data = parse_config(args)  # Parse YAML config
    except ConfigFileDoesNotExist as e:
        print(f"Error: {e.message}")
        return
    except ConfigMissingFields as e:
        print(f"Error: {e.message}")
        return
    except ConfigException as e:
        print(f"Error: {e.message}")
        return

    chat_name = args.chatname[0]
    days = int(args.days_delete[0])

    if days <= 0:  # In case days_delete <= 0
        print("Error: -days/--days_delete argument must be higher than 0")
        return

    try:
        await delete_messages(data, chat_name, days)
    except DialogNotFound as e:
        print(f"Error: {e.message}")
    except ApiIdInvalidError as e:
        print(f"Error: {str(e)}")
    except PhoneNumberInvalidError as e:
        print(f"Error: {str(e)}")
    except Exception as e:
        print(f"Error: {str(e)}, probably config file has errors")

if __name__ == "__main__":
    asyncio.run(main())
