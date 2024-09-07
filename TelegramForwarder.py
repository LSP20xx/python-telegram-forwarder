import time
import asyncio
import platform
import csv
from telethon.sync import TelegramClient
from telethon.errors import FloodWaitError, RPCError

class TelegramForwarder:
    def __init__(self, api_id, api_hash, phone_number):
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone_number = phone_number
        self.client = TelegramClient('session_' + phone_number, api_id, api_hash)

    async def list_chats(self):
        await self.client.connect()

        if not await self.client.is_user_authorized():
            await self.client.send_code_request(self.phone_number)
            await self.client.sign_in(self.phone_number, input('Enter the code: '))

        dialogs = await self.client.get_dialogs()

        encoding = 'utf-8' if platform.system() == 'Windows' else None

        with open(f"chats_of_{self.phone_number}.txt", "w", encoding=encoding) as chats_file:
            for dialog in dialogs:
                print(f"Chat ID: {dialog.id}, Title: {dialog.title}")
                chats_file.write(f"Chat ID: {dialog.id}, Title: {dialog.title} \n")

        print("List of chats printed successfully!")

    async def forward_messages_to_channel(self, source_chat_id, destination_channel_id, keywords):
        await self.client.connect()

        if not await self.client.is_user_authorized():
            await self.client.send_code_request(self.phone_number)
            await self.client.sign_in(self.phone_number, input('Enter the code: '))

        last_message_id = (await self.client.get_messages(source_chat_id, limit=1))[0].id

        while True:
            print("Checking for messages and forwarding them...")
            messages = await self.client.get_messages(source_chat_id, min_id=last_message_id, limit=None)

            for message in reversed(messages):
                if keywords:
                    if message.text and any(keyword in message.text.lower() for keyword in keywords):
                        print(f"Message contains a keyword: {message.text}")
                        await self.client.send_message(destination_channel_id, message.text)
                        print("Message forwarded")
                else:
                    await self.client.send_message(destination_channel_id, message.text)
                    print("Message forwarded")

                last_message_id = max(last_message_id, message.id)

            await asyncio.sleep(5)  # Adjust the delay time as needed

    async def download_messages_to_csv(self, chat_id):
        await self.client.connect()

        if not await self.client.is_user_authorized():
            await self.client.send_code_request(self.phone_number)
            await self.client.sign_in(self.phone_number, input('Enter the code: '))

        encoding = 'utf-8' if platform.system() == 'Windows' else None

        try:
            dialogs = await self.client.get_dialogs()

            entity = None
            for dialog in dialogs:
                if str(dialog.id) == str(chat_id) or dialog.name == chat_id:
                    entity = dialog.entity
                    break

            if not entity:
                print(f"Error: Could not find chat with ID or username '{chat_id}'.")
                return

            with open(f"messages_from_{chat_id}.csv", mode='w', newline='', encoding=encoding) as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(["Date", "Sender ID", "Message Text"])

                async for message in self.client.iter_messages(entity):
                    writer.writerow([message.date, message.sender_id, message.text])

            print("Messages downloaded successfully!")

        except RPCError as e:
            print(f"RPC Error: {e}")
        except ValueError as e:
            print(f"Error: {e}. Check if the chat ID is correct and accessible.")

# Function to read credentials from file
def read_credentials():
    try:
        with open("credentials.txt", "r") as file:
            lines = file.readlines()
            api_id = lines[0].strip()
            api_hash = lines[1].strip()
            phone_number = lines[2].strip()
            return api_id, api_hash, phone_number
    except FileNotFoundError:
        print("Credentials file not found.")
        return None, None, None

# Function to write credentials to file
def write_credentials(api_id, api_hash, phone_number):
    with open("credentials.txt", "w") as file:
        file.write(api_id + "\n")
        file.write(api_hash + "\n")
        file.write(phone_number + "\n")

async def main():
    api_id, api_hash, phone_number = read_credentials()

    if api_id is None or api_hash is None or phone_number is None:
        api_id = input("Enter your API ID: ")
        api_hash = input("Enter your API Hash: ")
        phone_number = input("Enter your phone number: ")
        write_credentials(api_id, api_hash, phone_number)

    forwarder = TelegramForwarder(api_id, api_hash, phone_number)
    
    print("Choose an option:")
    print("1. List Chats")
    print("2. Forward Messages to a Destination Chat")
    print("3. Download All Messages from a Chat to CSV")
    
    choice = input("Enter your choice: ")
    
    if choice == "1":
        await forwarder.list_chats()
    elif choice == "2":
        source_chat_id = input("Enter the source chat ID or username (for forwarding): ")
        destination_channel_id = input("Enter the destination chat ID or username (for forwarding): ")
        keywords = input("Put keywords (comma separated if multiple, or leave blank): ").split(",")
        await forwarder.forward_messages_to_channel(source_chat_id, destination_channel_id, keywords)
    elif choice == "3":
        chat_id = input("Enter the chat ID or username from which you want to download all messages to CSV: ")
        await forwarder.download_messages_to_csv(chat_id)
    else:
        print("Invalid choice")

if __name__ == "__main__":
    asyncio.run(main())
