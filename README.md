# taust-client

**taust-client allows to monitor some metrics of a server (CPU, memory and
disks space).** You’ll need a running instance of [taust](https://github.com/flusio/taust)
to be able to use taust-client.

taust-client is written in Python and is licensed under [AGPL 3](./LICENSE).

**taust is now done. It means no new feature will be added, but it’s still
maintained.** I’ve been using it for few years and I’m happy with the current
version. However, I may encounter some bugs or security issues: I intend to fix
them.

## Installation

Clone the repository on your server:

```console
# git clone https://github.com/flusio/taust-client.git /opt/taust-client
```

Install dependencies, e.g. for Debian:

```console
# apt install python3-dev gcc
# pip3 install -r /opt/taust-client/requirements.txt
```

Add a server to monitor on your taust instance and copy the token it gives
you. Then, create a `.env` file:

```console
# vim /opt/taust-client/.env
# chmod 400 /opt/taust-client/.env
```

```env
ENDPOINT=https://your-taust-instance.example.org
AUTH_TOKEN=the-taust-token
```

If you want to monitor specific disks instead of letting taust discover them,
set a `DISKS` environment variable in this same file. Disks are separated by
commas:

```env
DISKS=/dev/sda1,/dev/sdb1
```

Finally, setup a systemd file:

```console
# vim /etc/systemd/system/taust-client.service
```

```systemd
[Unit]
Description=Taust service
After=network.target

[Service]
Type=simple
WorkingDirectory=/opt/taust-client
ExecStart=python3 taust.py

Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
```

Start taust-client:

```console
# systemctl start taust-client
# systemctl enable taust-client
```
