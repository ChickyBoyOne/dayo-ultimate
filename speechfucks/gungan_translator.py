from bs4 import BeautifulSoup, SoupStrainer
import httpx
from telethon.tl.custom.message import Message

NAME = "Gungan Translator"
ID = "gungan_translator"

# Run message through https://talklikejarjarday.com/gungan_translator/
async def on_outgoing_message(message: Message):
    text = message.message
    if not text:
        return
    
    async with httpx.AsyncClient() as client:
        r = await client.post("https://talklikejarjarday.com/gungan_translator/", data={"translatebox": text})
    r.raise_for_status()

    only_translation = SoupStrainer(id="the_translation")
    soup = BeautifulSoup(r.text, "lxml", parse_only=only_translation)
    translation = soup.find(id="the_translation").get_text().strip()
    await message.edit(translation)
