# Feel free to edit the options below!

# Select the amount of SFX you want!
# Can be "none", "some", or "constant"
SFX_AMOUNT = "none"

# Select what SFX you want!
# Can be True or False

# Toggle Burp & Moan SFX
SFX_BURP_AND_MOAN = True
# Toggle Eating SFX
SFX_EATING = False
# Toggle Toot SFX
SFX_TOOT = False

# Add these to make your blob slur their words!
# Can be True or False

# Toggle extra 'h' after Vowels
SLUR_EXTRA_H_AFTER_VOWELS = False
# Toggle extra Vowels
SLUR_EXTRA_VOWELS = False
# Toggle Burp Interupts
SLUR_BURP_INTERRUPTS = False

# == END OPTIONS SECTION - DO NOT EDIT BELOW UNLESS YOU KNOW WHAT YOU'RE DOING ==

from pathlib import Path
import re

import hishel
import pythonmonkey as pm
from telethon.tl.custom.message import Message

NAME = "Fat Text Generator by SkeleSoda"

SELF = Path(__file__)
DATA_DIR = SELF.parent / (SELF.stem + "_data")

# Get the fat text generator code from SkeleSoda on itch.io: https://skelesoda.itch.io/fat-speak-translator
async def setup():
    DATA_DIR.mkdir(exist_ok=True)

    storage = hishel.AsyncFileStorage(base_path=DATA_DIR / "cache")
    async with hishel.AsyncCacheClient(storage=storage) as client:
        page = await client.get("https://html-classic.itch.zone/html/9904858/index.html")
    page.raise_for_status()
    text = page.text

    script_match = re.search(r"(?s)<script>(?P<script>.*?)<\/script>", text)
    if not script_match:
        raise Exception(f"Could not match script in Fat Speak Translator page! {text}")
    script = script_match.group("script")

    if SFX_AMOUNT not in ["none", "some", "constant"]:
        raise Exception(f"SFX_AMOUNT contains an invalid string: {SFX_AMOUNT}")

    options = {
        "iCheckbox1": SFX_AMOUNT == "none",
        "iCheckbox2": SFX_AMOUNT == "some",
        "iCheckbox3": SFX_AMOUNT == "constant",
        "sfxCheckbox": SFX_BURP_AND_MOAN,
        "eatCheckbox": SFX_EATING,
        "tootCheckbox": SFX_TOOT,
        "toggleCheckbox2": SLUR_EXTRA_H_AFTER_VOWELS,
        "toggleCheckbox1": SLUR_EXTRA_VOWELS,
        "toggleCheckbox5": SLUR_BURP_INTERRUPTS,
    }
    pm.globalThis.update({key: {"checked": value} for key, value in options.items()})
    pm.eval("document = {getElementById: (id) => globalThis[id]}")

    pm.eval(script)

async def on_outgoing_message(message: Message):
    fat_text = pm.globalThis["translate"](message.message)
    await message.edit(fat_text)
