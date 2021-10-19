#!/bin/env python3

import psutil
import time
import json
import urllib.request
import urllib.error
import base64
import socket
import syslog


def start(endpoint, auth_token, default_disks_to_monitor):
    # First call with interval=None is meaningless, we should drop it
    psutil.cpu_percent(interval=None, percpu=True)

    hostname = socket.gethostname()
    credentials = hostname + ":" + auth_token
    headers = {
        "Authorization": "Basic " + base64.b64encode(credentials.encode()).decode()
    }

    while True:
        time.sleep(10)

        if default_disks_to_monitor:
            disks_to_monitor = default_disks_to_monitor
        else:
            disk_partitions = psutil.disk_partitions()
            disks_to_monitor = [
                disk_partition.mountpoint for disk_partition in disk_partitions
            ]

        disks = []
        for disk_name in disks_to_monitor:
            disk_usage = psutil.disk_usage(disk_name)
            disks.append(
                {"name": disk_name, "total": disk_usage.total, "free": disk_usage.free}
            )

        memory = psutil.virtual_memory()

        payload = json.dumps(
            {
                "at": int(time.time()),
                "cpu_percent": psutil.cpu_percent(interval=None, percpu=True),
                "memory_total": memory.total,
                "memory_available": memory.available,
                "disks": disks,
            }
        )

        try:
            request = urllib.request.Request(endpoint, payload.encode(), headers)
            response = urllib.request.urlopen(request).read().decode()
        except urllib.error.URLError as e:
            syslog.syslog(syslog.LOG_ERR, str(e))


if __name__ == "__main__":
    with open(".env", "r") as dotenv_file:
        dotenv_content = dotenv_file.read()

    env = {}
    for line in dotenv_content.splitlines():
        line = line.strip()
        key, value = line.split("=")
        env[key] = value

    endpoint = env["ENDPOINT"]
    auth_token = env["AUTH_TOKEN"]
    disks = env.get("DISKS", "")
    disks = [d.strip() for d in disks.split(",") if d.strip()]

    syslog.syslog(f"Starting taust… it will send payloads to {endpoint}")
    start(endpoint, auth_token, disks)
