
load("@io_bazel_rules_docker//container:container.bzl", "container_image")

container_image(
    name = "hello_project_image",
    base = "@python//image:3.10-slim-buster",
    env = {
        "VENV": "/opt/venv",
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "PYTHONPATH": "/root",
        "PATH": "/opt/venv/bin:$PATH",
    },
    directory = "/root",
    tars = [
        "//:requirements.txt",
    ],
    cmd = [
        "bash", "-c",
        "apt-get update && apt-get install -y build-essential && "
        "python3 -m venv /opt/venv && "
        "pip install -r /root/requirements.txt && "
        "cp -r . /root"
    ],
)
