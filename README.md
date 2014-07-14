Pidora v2 Pre-Alpha README
==========================

**Danger, Will Robinson!** Please note this is the README for Pidora v2. You can download the more stable v1.0-final [here](https://github.com/jacroe/pidora/releases/tag/v1.1-final).

Setup
-----

1. Unzip the contents. If you're reading this you've obviously got a handle on decompressing files so head on over to Step 2.
2. Register for a free API key for Last.fm's api. You'll use this to get the albumart for Soma.fm. You can access that at [http://www.last.fm/api](http://www.last.fm/api). Plug in your key in the appropriate field in `config.json`.
3. Move your FIFO to your Pianobar config directory (e.g. `/home/jacob/.config/pianobar/ctl`) and update that location in the config as well. 
4. That should be it. Run `hello.py` to start Pidora v2.


Notes
-----

Pidora v2 has a much better API than v1. However, it's not documented yet. I've included some initial documentation in the `docs/` folder, but it's very incomplete and hard to understand. This will be flushed out soon. If you're feeling really ambitious, you check out the API code in `hello.py` and see how it works. It's a whole lot less clunky than in v1.