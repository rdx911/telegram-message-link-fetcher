Telethon User Guide

Introduction
------------
This script uses the Telethon library to fetch message links from a specified Telegram channel.

Prerequisites
-------------
- Python 3.7+ installed
- Install Telethon:
  pip install telethon
- API ID & API Hash from https://my.telegram.org/apps

Configuration
-------------
Replace the placeholders in the script with your API details:

SESSION_NAME = "session_name"
api_id = 1234567  # Replace with your API ID
api_hash = "74839201563728495012643895720163"  # Replace with your API Hash

How to Run the Script
---------------------
1. Run:
   python script.py
2. Enter the Channel ID (You can extract it from the channel URL, e.g., 
   https://web.telegram.org/a/#-1002593909874
   The Channel ID is -1002593909874.)
3. Choose mode:
   - all: Fetches all available messages.
   - range: Enter a start and end message ID to fetch only a particular range.
   (Extract message ID from message link, e.g., 
   https://t.me/c/123456789/99
   The message ID is 99.)

Data Source
-----------
The script fetches messages from Telegram channels using the Telethon API.

Output
------
Extracted message links are saved in:
channel_<channel_id>.txt

Error Handling
--------------
Error: FloodWaitError - Waits before retrying
Error: ChatAdminRequiredError - Bot lacks admin rights
Error: ChannelPrivateError - Cannot access private channel
Error: SessionPasswordNeededError - Two-step verification enabled

Conclusion
----------
This script simplifies Telegram message link extraction. For more details, visit:
https://docs.telethon.dev/
