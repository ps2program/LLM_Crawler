import os

# Authenticate ngrok
os.system("ngrok config add-authtoken 2ktHyyR9SposgnCNT0PfEhCtcQH_4ZfsYPCAbt87wZv7Uojqy")

# Start ngrok tunnel
os.system("ngrok http --url=major-legible-walrus.ngrok-free.app 1234")
