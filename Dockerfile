FROM python:3.10.5-alpine3.15

ARG VERSION_ARG=unknown
ENV VERSION=$VERSION_ARG

LABEL org.opencontainers.image.source https://github.com/belarusians/contact-bot
ENV USER=botuser \
    GROUP=botgroup

COPY ./requirements.txt /bot/

RUN addgroup -S ${GROUP} && \
    adduser -S ${USER} ${GROUP} && \
    chown ${USER}:${GROUP} /bot

WORKDIR /bot

RUN pip install -r requirements.txt

COPY ./src /bot/src

USER ${USER}

ENTRYPOINT [ "python", "./src/bot.py" ]
