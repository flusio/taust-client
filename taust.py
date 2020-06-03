#!/bin/env python3

import psutil
import time
import json
import urllib.request
import urllib.error
import base64
import socket


def start(endpoint, auth_token):
    # First call with interval=None is meaningless, we should drop it
    psutil.cpu_percent(interval=None, percpu=True)

    hostname = socket.gethostname()
    credentials = hostname + ":" + auth_token
    headers = {
        "Authorization": "Basic " + base64.b64encode(credentials.encode()).decode()
    }

    while True:
        time.sleep(10)

        memory = psutil.virtual_memory()
        disks = []
        disk_partitions = psutil.disk_partitions()
        for disk_partition in disk_partitions:
            disk_name = disk_partition.mountpoint
            disk_usage = psutil.disk_usage(disk_name)
            disks.append(
                {"name": disk_name, "total": disk_usage.total, "free": disk_usage.free}
            )

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
            # TODO log the error and try to send it to the server
            print(e)


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

    print(f"Starting taust… it will send payloads to {endpoint}")
    start(endpoint, auth_token)
