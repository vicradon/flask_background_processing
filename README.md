# Flask Background Processing - HNG Task 3

This is a background processing app built with Flask that uses RabbitMQ and Celery to handle background processing.

## Setting up

To set it up, edit the `scripts/changeowner.sh` and add the default user of the computer and its group on line 2. Then run the following scripts in order:

```sh
sudo bash scripts/installrabbit.sh
sudo bash scripts/changeowner.sh
bash scripts/setupapp.sh
```

### Setting up the environment

After this basic setup is complete, you should create the required environment variables. This application uses Mailtrap for email sending, so you need a mailtrap user and password. Refer to [this guide](https://help.mailtrap.io/article/69-sending-domain-setup) to obtain yours. Create the `.env` file from the `.env.example` by duplicating the later or using this command: `cp .env.example .env`. Afterwards, fill in the appropriate details:

```.env
MAILTRAP_USER="api"
MAILTRAP_PASSWORD="your_secret"
SOCKET_SECRET="I_LOVE_SECRETS"
```

The socket secret is to be used by socket.io because this application does live logging.

### Running the application

You could run the app in two ways, either managed using pm2 which can handle starts and restarts, or by running the scripts/runflask.sh directly. To run using pm2, ensure you have node.js installed, version 20 or higher. The snippet below installs pm2 globally and runs the app in backgroun:

```sh
npm i -g pm2
pm2 start pm2.config.js
pm2 save
pm2 list
```

If you wish to run directly, simly run `bash scripts/runflask.sh`

PS: if you want to run locally, you can simply source the environment and use python app.py like so:

```sh
source .venv/bin/activate
python app.py
```

## Setting up Nginx reverse proxy

With the app running on port 5000, you can use Nginx to reverse proxy it on port 80. Do it like so:

```sh
sudo bash scripts/createnginxconfig.sh
```

The script creates the nginx config and reverse proxies the app on port 80.

## Forwarding via Ngrok

You can forward the application running on port 80 via

```
ngrok http 80
```

If you want to run in a screen, use:

```sh
First run it
screen -S myngrok
ngrok http 800
Ctrl A Ctrl D # detach from screen
```

To list all screens:

```sh
screen -ls
```

to reattach to the screen:

```sh
screen -r myngrok
# or screen -r <screen_number>
```

## Contributing

Erm...
