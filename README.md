# Telegram Message Remover
CLI that Removes all the messages from the telegram chat starting from given number of days

### Requirements
- python 3.9
- pip3
- git

## How to start
- Clone the repo
> $ git clone "https://github.com/NotVeryWellF/telegram_message_remover.git" \
> $ cd telegram_message_remover
- Install python requirements
> $ pip3 install -r requirements.txt
  - Fill all the fields in YAML config file \
    You can see the template in config_template.yml
    ```
    data:
      api_id: api_id
      api_hash: api_hash
      phone: phone_number
      username: username
    ```
  - Now you can start removing messages
> $ python3 remover.py [commands]
- Example
> $ python3 remover.py -chn "SomeChat" -cfg config.yml -days 100

## Help
```
$ python3 remover.py --help
usage: remover.py [-h] -chn chat -cfg config_file [-days days_to_delete]

message remover from telegram chat

optional arguments:
  -h, --help            show this help message and exit
  -chn chat, --chatname chat
                        Name of the chat, in which the messages will be removed
  -cfg config_file, --config_file config_file
                        Config file with: api_id, api_hash, phone, username. Format: .yml, .yaml
  -days days_to_delete, --days_delete days_to_delete
                        From how many days ago start deleting messages. Default: 60 days

```