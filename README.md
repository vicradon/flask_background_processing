# Flask Background Processing - HNG Task 3

This is a background processing app built with Flask that uses RabbitMQ and Celery to handle background processing.

## Prerequistes

This application is primarily set up to run on a Linux system, particularly Ubuntu. If you desire to run it on a different system, ensure the scripts within the scripts directory match your OS.

## Setting up

To set it up, edit the `scripts/changeowner.sh` and add the default user of the computer and its group on line 2 `sudo chown osi:osi /var/log/messaging_system.log`. Then run the following scripts in order:

```sh
sudo bash scripts/installrabbit.sh
sudo bash scripts/changeowner.sh
bash scripts/setupapp.sh
```

### Setting up the environment

After this basic setup is complete, you should create the required environment variables. This application uses Python's standard SMTP lib and Mailtrap for email sending, so you need a mailtrap user and password. Refer to [this guide](https://help.mailtrap.io/article/69-sending-domain-setup) to obtain yours. Create the `.env` file from the `.env.example` by duplicating the later or using this command: `cp .env.example .env`. Afterwards, fill in the appropriate details:

```.env
MAILTRAP_USER="api"
MAILTRAP_PASSWORD="your_secret"
SOCKET_SECRET="I_LOVE_SECRETS"
```

The socket secret is to be used by socket.io because this application does live logging.

### Running the application

You could run the app in two ways, either managed using pm2 which can handle starts and restarts, or by running the scripts/run_flask_and_celery.sh directly. To run using pm2, ensure you have node.js installed, version 20 or higher. The snippet below installs pm2 globally and runs the app in background:

```sh
npm i -g pm2
pm2 start pm2.config.js
pm2 save
pm2 list
```

If you wish to run directly, simly run `bash scripts/run_flask_and_celery.sh`

PS: if you want to run the development server, you can simply source the environment and use python app.py like so:

```sh
source .venv/bin/activate
python app.py
```

## Setting up Nginx reverse proxy

With the app running on port 5000, you can use Nginx to reverse proxy it to port 80. The script `createnginxconfig.sh` in the scripts directory sets up the Nginx config for this app and reloads the Nginx configuration so that as Nginx runs in the background, it proxies the application from port 5000 to port 80. Run the script using the command below:

```sh
sudo bash scripts/createnginxconfig.sh
```

## Forwarding via Ngrok

You can forward the application to the internet using Ngrok. All you need to do is run the command below:

```
ngrok http 80
```

The command above runs Ngrok in a non-exit terminal. If you close the terminal, your Ngrok session terminates. It's cleaner to run Ngrok in a separate screen. You can use the sequence of commands below to achieve this:

```sh
screen -S myngrok

# within the screen
ngrok http 800

# detach from the screen
Ctrl A Ctrl D
```

To list all screens:

```sh
screen -ls
```

to re-attach to the screen:

## Contributing

Erm...
