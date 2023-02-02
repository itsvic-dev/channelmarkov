#!/usr/bin/env python3
import microinvidious
import logging
import socket
import config

logging.basicConfig(format='[%(levelname)s / %(asctime)s] %(message)s', level=logging.INFO)

instance = config.INVIDIOUS_INSTANCE

user_channels = config.SCRAPE_CHANNELS["user"]
channels = config.SCRAPE_CHANNELS["c"]
id_channels = config.SCRAPE_CHANNELS["channel"]

def save_titles(channel: str, titles: list):
    with open(f"data/{channel}.txt", 'w+') as file:
        file.write("\n".join(titles))

for channel in channels:
    logging.info("Downloading titles for %s...", channel)
    try:
        save_titles(channel, microinvidious.parse_c(channel, instance))
    except Exception as e:
        logging.warn("Failed to download titles for %s.", channel)
        print(e)

for channel in user_channels:
    logging.info("Downloading titles for %s...", channel)
    try:
        save_titles(channel, microinvidious.parse_user(channel, instance))
    except Exception as e:
        logging.warn("Failed to download titles for %s.", channel)
        print(e)

for channel in id_channels:
    logging.info("Downloading titles for %s...", channel)
    try:
        save_titles(channel, microinvidious.parse_channel(channel, instance))
    except Exception as e:
        logging.warn("Failed to download titles for %s.", channel)
        print(e)
