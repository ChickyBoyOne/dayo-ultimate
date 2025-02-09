# Feel free to edit the options below!

# Can be none, some, or constant
SFX_AMOUNT = "none"

SFX_BURP_AND_MOAN = True
SFX_EATING = False
SFX_TOOT = False

SLUR_EXTRA_H_AFTER_VOWELS = False
SLUR_EXTRA_VOWELS = False
SLUR_BURP_INTERRUPTS = False

# == END OPTIONS SECTION - DO NOT EDIT BELOW UNLESS YOU KNOW WHAT YOU'RE DOING ==

from pathlib import Path
import re

import hishel
import pythonmonkey as pm
from telethon.tl.custom.message import Message

NAME = "Fat Text Generator by SkeleSoda"
ID = "fat_text_generator"

DATA_DIR = Path(__file__).parent / (ID + "_data")
script = None

PRELUDE = """
document = {}

document.getElement
"""

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