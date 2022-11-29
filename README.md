[![Build and push docker image](https://github.com/belarusians/some_bot/actions/workflows/ci-build.yml/badge.svg)](https://github.com/belarusians/some_bot/actions/workflows/ci-build.yml)

# Repository for some_bot

### Prerequisites
To run in docker:
* docker

To run locally:
* python 3 (checked only 3.10)

### Run

1. pull image:
    `docker pull ghcr.io/belarusians/some_bot:latest`

2. run first time for getting settings
    `docker run ghcr.io/belarusians/some_bot "%TELEGRAM_API_KEY%"`

3. add bot to your admin group and wait for the message like that:
    ```text
    ADMIN_GROUP: -807787002
    Перазапусьціце мяне з гэтым параметрам, каб я змог сюды пісаць
    ```

4. rerun bot in the following way:
    `docker run -e ADMIN_GROUP="%ADMIN_GROUP%" ghcr.io/belarusians/some_bot "%TELEGRAM_API_KEY%"`

### Build and locally in docker

`docker build -t="SOME_NAME" .`
`docker run -it SOME_NAME`
