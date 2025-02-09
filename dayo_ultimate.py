import asyncio
import importlib
import pkgutil

from telethon import events, TelegramClient
import telethon.tl.custom as tl

from telegram_secrets import API_HASH, API_ID

async def NOOP_0():
    return
async def NOOP_1(_):
    return
STOP = "/stop"

async def provide_feedback_and_delete(message: tl.message.Message, feedback: str):
    await message.edit(feedback)
    await asyncio.sleep(1.5)
    await message.delete()

async def main():
    active_chats = {}
    all_speechfucks = {}
    speechfuck_search = {}

    for _, speechfuck_id, _ in pkgutil.iter_modules(["speechfucks"]):
        speechfuck = importlib.import_module(f"speechfucks.{speechfuck_id}")
        all_speechfucks[speechfuck_id] = speechfuck
        speechfuck_search[speechfuck_id] = speechfuck_id
        speechfuck_search[speechfuck.NAME.lower()] = speechfuck_id
        await getattr(speechfuck, "setup", NOOP_0)()

    if all_speechfucks:
        print("Speechfucks loaded:")
        for speechfuck_id, speechfuck in all_speechfucks.items():
            print(f" - {speechfuck.NAME} ({speechfuck_id})")
    else:
        print("No speechfucks loaded!")

    client = TelegramClient("telegram_account", API_ID, API_HASH)
    await client.start(phone=lambda: input("Please enter your phone in international format, e.g. +12345678910: "))

    @client.on(events.NewMessage(outgoing=True, pattern=STOP))
    async def stop_handler(event: events.NewMessage.Event):
        message: tl.message.Message = event.message
        text = message.message
        if text != STOP:
            return
        
        if message.chat_id not in active_chats:
            await provide_feedback_and_delete(message, "No speechfuck has been started for this chat!")
            return

        await provide_feedback_and_delete(message, f"Stopping speechfuck {active_chats[message.chat_id].NAME}!")
        del active_chats[message.chat_id]
    
    @client.on(events.NewMessage)
    async def message_handler(event: events.NewMessage.Event):
        message: tl.message.Message = event.message
        if message.chat_id not in active_chats:
            return
        
        speechfuck = active_chats[message.chat_id]
        await getattr(speechfuck, "on_message", NOOP_1)(message)
        if message.out:
            await getattr(speechfuck, "on_outgoing_message", NOOP_1)(message)
        else:
            await getattr(speechfuck, "on_incoming_message", NOOP_1)(message)

    @client.on(events.NewMessage(outgoing=True, pattern="/start "))
    async def start_handler(event: events.NewMessage.Event):
        message: tl.message.Message = event.message
        text = message.message
        if not text:
            return
        split = text.split(" ")
        if len(split) != 2:
            return
        speechfuck_id = split[1]
        if speechfuck_id not in all_speechfucks:
            possibilities = set()

            for possibility, possibility_id in speechfuck_search.items():
                if speechfuck_id in possibility:
                    possibilities.add(possibility_id)
            
            num_possibilities = len(possibilities)
            if num_possibilities == 1:
                speechfuck_id = next(iter(possibilities))
            elif num_possibilities > 1:
                feedback = f"Multiple possibilities for speechfuck `{speechfuck_id}`:\n"
                for possibility in possibilities:
                    speechfuck = all_speechfucks[possibility]
                    feedback += f" - {speechfuck.NAME} (`{possibility}`)"
                await provide_feedback_and_delete(message, feedback)
                return
            else:
                await provide_feedback_and_delete(message, f"Couldn't find speechfuck `{speechfuck_id}`!")
                return
        
        speechfuck = all_speechfucks[speechfuck_id]
        active_chats[message.chat_id] = speechfuck
        await provide_feedback_and_delete(message, f"Started speechfuck {speechfuck.NAME}!")
    
    await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
