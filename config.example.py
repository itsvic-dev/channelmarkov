# This is an example configuration file for ChannelMarkov.

# Main script settings
## Mastodon APIv2 OAuth2 secrets
OAUTH_CLIENT_ID="id"
OAUTH_CLIENT_SECRET="secret"

## Mastodon instance.
MASTODON_INSTANCE="https://botsin.space"

## Datasets used by the 2 different scripts.
WINTUBER_DATASETS = {
    "Example": "example",
}

YOUTUBER_DATASETS = {
    "Tom Scott": "TomScott",
}

# Scrape script settings
## Invidious instance to use for scraping titles.
## You should preferably use a local instance for better speeds.
INVIDIOUS_INSTANCE="https://inv.omame.xyz"

## Channels to scrape.
SCRAPE_CHANNELS={
    "user": [  # youtube.com/user/{channel}
        "PewDiePie",
    ],
    "c": [  # youtube.com/c/{channel}
        "TomScott",
    ],
    "channel": [  # youtube.com/channel/{channelID}
    ],
}
