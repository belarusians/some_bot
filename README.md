[![Build and push docker image](https://github.com/belarusians/some_bot/actions/workflows/ci-build.yml/badge.svg)](https://github.com/belarusians/some_bot/actions/workflows/ci-build.yml)

# Repository for some_bot

### Prerequisites
* docker
* python 3.10

### Build

`docker build -t="SOME_NAME" .`

### Run

First you need to just run bot:
`docker run %SOME_NAME% "%TELEGRAM_API_KEY%"`

Then add it to your admin group and wait for the message like that:

```text
ADMIN_GROUP: -807787002
Перазапусьціце мяне з гэтым параметрам, каб я змог сюды пісаць
```

Then you need to rerun bot in the following way:

`docker run -e ADMIN_GROUP="%ADMIN_GROUP%" SOME_NAME "%TELEGRAM_API_KEY%"`

