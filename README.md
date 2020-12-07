# server-creeper
A bot to manage my Minecraft server on a Google Cloud Compute instance.

Before you start, you will need 4 things:
1) A functioning Google Cloud Compute instance with your server on it, configured to start the server upon starting the VM. (See https://cloud.google.com/solutions/gaming/minecraft-server)
2) A JSON file named creds.json containing the credentials of a service account with permissions to operate on your VM. (See https://cloud.google.com/docs/authentication/production#create_service_account)
3) A bot token from Discord for your Discord bot.
4) Some place to host this code (Personally, I just use another free Google f1-micro VM instance).

Once you have these, simply fill in the bot_token, project, zone, and instance variables in main.py, and run the bot. 