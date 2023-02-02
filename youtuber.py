#!/bin/python3
import markovify
import random
import time
import microdon
import config

datasets = config.YOUTUBER_DATASETS
markov_models = {}

for key, value in datasets.items():
    with open(f"data/{value}.txt") as file:
        markov_models[key] = markovify.NewlineText(file.read()).compile(inplace=True)

if False:  # disable merged datasets since they make no sense here
    merged_datasets = {}

    for key, value in datasets.items():
        for other_key, other_value in datasets.items():
            if (key == other_key or
                f"{key} and {other_key}" in merged_datasets or
                f"{other_key} and {key}" in merged_datasets):
                continue
            merged_datasets.update({
                f"{key} and {other_key}": markovify.NewlineText(
                    open(f"data/{value}.txt").read() + open(f"data/{other_value}.txt").read()
                ).compile(inplace=True)
            })

    markov_models.update(merged_datasets)

def get_random_quote():
    key, model = random.choice(list(markov_models.items()))
    quote = model.make_sentence()
    if quote is None:
        return None
    return key, quote

client = microdon.MastodonOAuth2("youtuber", config.MASTODON_INSTANCE, config.OAUTH_CLIENT_ID, config.OAUTH_CLIENT_SECRET)

while True:
    client.check_auth()
    quote = None
    while quote is None:
        quote = get_random_quote()
    client.send_toot(f"{quote[1]}\nby {quote[0]}\n\n#markov")
    print(quote[0], "->", quote[1])
    time.sleep(1 * 60 * 30)  # 30 minutes
