import microdon
import config

client = microdon.MastodonOAuth2("test", config.MASTODON_INSTANCE, config.OAUTH_CLIENT_ID, config.OAUTH_CLIENT_SECRET)
client.check_auth()

client.send_toot("hi from microdon!")
