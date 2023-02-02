# ChannelMarkov

This repository contains cleaned up source code for my two Twitter bots,
[@MWintuber](https://twitter.com/MWintuber) and [@markovtube](https://twitter.com/markovtube).

The only changes from the original are the removal of hard-coded variables,
instead replaced with a `config.py` file.

This source code **will not** be maintained unless specified otherwise.  
In theory it should Just Work™, but if you don't have an API license (February 9th changes),
this code will most likely not work out of the box.

With that said however, **I will not provide support for this. You are on your own.**

## How to run

1. **Write a configuration file.**  
   Copy `config.example.py` into `config.py`. Fill out stuff such as the channels you want to use, as well as OAuth2 information.

2. **Install dependencies.**  
   Run `pip install -r requirements.txt`.

3. **Run the script(s).**  
   Choose either `wintuber.py` or `youtuber.py` (they behave slightly differently!), run them, and follow the instructions on screen.
