# Setup

## Django

create virtual environment `venv` and activate it

    virtualnev venv
    source venv/bin/activate

Create file `config.ini` inside `venv` with following structure

    [django]
    SECRET_KEY:<long random string>
    HOST:www.generaltech.in,generaltech.in

Create directory for static files

    mkdir static

Initiate django

    ./manage.py migrate
    ./manage.py collectstatic

## Server

Create Socket File

    sudo nano /etc/systemd/system/generaltech.socket

Add following in the file

    [Unit]
    Description=generaltech socket

    [Socket]
    ListenStream=/run/generaltech.sock

    [Install]
    WantedBy=sockets.target

Create service file

    sudo nano /etc/systemd/system/generaltech.service

Add follwing in the file

    [Unit]
    Description=GeneralTech Website
    Requires=generaltech.socket
    After=network.target

    [Service]
    User=mukul
    Group=www-data
    WorkingDirectory=/home/mukul/inception_general_tech_website
    ExecStart=/home/mukul/inception_general_tech_website/venv/bin/gunicorn \
                    --access-logfile - \
                    --workers 3 \
                    --bind unix:/run/generaltech.sock \
                    generaltech.wsgi:application

    [Install]
    WantedBy=multi-user.target

Now start and enable the generaltech socket. This will create the socket file at `/run/generaltech.sock` now and at boot. When a connection is made to that socket, systemd will automatically start the `generaltech.service` to handle it.

    sudo systemctl start generaltech.socket
    sudo systemctl enable generaltech.socket

Check the status of the socket

    sudo systemctl status generaltech.socket

Next, check for the existence of the `generaltech.sock` file within the `/run` directory

    file /run/generaltech.sock

If the `systemctl status` command indicated that an error occurred or if you do not find the `generaltech.sock` file in the directory, it’s an indication that the generaltech socket was not able to be created correctly. Check the generaltech socket’s logs by typing

    sudo journalctl -u generaltech.socket

## Nginx

Add the following inside your nginx server block

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }