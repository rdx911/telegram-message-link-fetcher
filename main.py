from telethon import TelegramClient, errors
import os
import asyncio

# Session & API Credentials
SESSION_NAME = "session_name"
api_id = 1234567  # Replace with your API ID
api_hash = "74839201563728495012643895720163"  # Replace with your API Hash

# Check if session exists
if os.path.exists(f"{SESSION_NAME}.session"):
    print("Existing session found. Logging in automatically...")
else:
    try:
        api_id = int(input("Enter your API ID: ")) if not api_id else api_id
        api_hash = input("Enter your API Hash: ") if not api_hash else api_hash
    except ValueError:
        print("Invalid input! API ID must be a number.")
        exit()

# Initialize Telegram Client
client = TelegramClient(SESSION_NAME, api_id, api_hash)

# Function to fetch messages
async def get_message_links(channel_id, start_from=None, end_at=None):
    try:
        await client.start()
        print(f"\nFetching messages from Channel ID: {channel_id}...\n")

        # Clean channel ID
        clean_channel_id = str(abs(channel_id)).replace("100", "", 1)
        filename = f"channel_{clean_channel_id}.txt"
        mode = "a" if os.path.exists(filename) else "w"
        
        last_message_id = None
        if os.path.exists(filename) and mode == "a":
            with open(filename, "r", encoding="utf-8") as file:
                lines = file.readlines()
                if lines:
                    last_message_id = int(lines[-1].strip().split("/")[-1])
                    print(f"Resuming from message ID: {last_message_id}")

        with open(filename, mode, encoding="utf-8") as file:
            async for message in client.iter_messages(channel_id, reverse=True):
                if start_from and message.id < start_from:
                    continue
                if end_at and message.id > end_at:
                    break
                if last_message_id and message.id <= last_message_id:
                    continue

                message_id = message.id
                message_link = f"https://t.me/c/{clean_channel_id}/{message_id}"
                print(message_link)
                file.write(message_link + "\n")

        print(f"\nAll links saved in {filename}\n")

    except errors.FloodWaitError as e:
        print(f"Too many requests! Waiting {e.seconds} seconds before retrying...")
        await asyncio.sleep(e.seconds)
        await get_message_links(channel_id, start_from, end_at)
    except errors.ChatAdminRequiredError:
        print("Bot does not have admin rights in this channel. Please check permissions.")
    except errors.ChannelPrivateError:
        print("Cannot access private channel. Make sure you have joined it.")
    except errors.SessionPasswordNeededError:
        print("Two-step verification is enabled. Please enter your password.")
    except errors.RPCError as e:
        print(f"Telegram API Error: {e}")
    except Exception as e:
        print(f"Unexpected Error: {e}")

# Main script execution
async def main():
    while True:
        try:
            channel_id = input("\nEnter the Channel ID (or type 0 to exit): ").strip()
            if channel_id == "0":
                break
            
            channel_id = int(channel_id)
            
            choice = input("Do you want to fetch all messages or from a specific range? (all/range): ").strip().lower()
            if choice == "range":
                start_from = int(input("Enter start message ID: "))
                end_at = int(input("Enter end message ID: "))
                await get_message_links(channel_id, start_from, end_at)
            else:
                await get_message_links(channel_id)
        
        except ValueError:
            print("Invalid input! Please enter valid numbers.")

# Run the script
with client:
    client.loop.run_until_complete(main())
