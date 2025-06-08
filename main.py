import requests
import threading
import time
from flask import Flask

app = Flask(__name__)

# Roblox user IDs to track
user_ids = [2346725415, 5589770247, 4456108587, 3023198676, 240311709]

# Your Discord webhook URL
webhook_url = "https://discord.com/api/webhooks/1381285268392251474/vwf_QLoXtHx8Sh67GlGV_9G83IFOBr2mPGgbMiTtnEeGcBEmPUCoRLS7RbQ2rkHhrBpH"

# Your Discord user ID (optional)
discord_user_id = 968508934249910273

# Store previous statuses
last_statuses = {}

# Human-readable status map
status_map = ["Offline", "Online", "In Game", "In Studio"]

def presence_tracker():
    global last_statuses
    while True:
        try:
            response = requests.post(
                "https://presence.roblox.com/v1/presence/users",
                json={"userIds": user_ids}
            )

            if response.status_code != 200:
                print(f"Error: {response.status_code} - {response.text}")
                time.sleep(60)
                continue

            user_data = response.json().get("userPresences", [])

            for user in user_data:
                user_id = user.get("userId")
                username = user.get("userName", f"User {user_id}")
                status = user.get("userPresenceType", 0)

                if user_id not in last_statuses or last_statuses[user_id] != status:
                    status_text = status_map[status]
                    mention = f"<@{discord_user_id}> " if discord_user_id else ""
                    msg = f"{mention}{username} is now **{status_text}**"

                    requests.post(webhook_url, json={"content": msg})
                    last_statuses[user_id] = status

        except Exception as e:
            print(f"Error: {e}")

        time.sleep(60)

@app.route("/")
def home():
    return "✅ Roblox Presence Tracker is running on Railway!"

# Start the tracker thread
threading.Thread(target=presence_tracker).start()

# Start the Flask server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
