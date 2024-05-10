FROM python:3.10.14-bookworm

LABEL authors="Suheel Hussain"

RUN apt-get -q -y update \
    && apt-get install net-tools

WORKDIR = /app

ENV USERNAME sshussain
ENV WORKING_DIR /home/sshussain

WORKDIR ${WORKING_DIR}

COPY src .
COPY requirements.txt .
COPY ./service_entrypoint.sh .

RUN groupadd ${USERNAME} && useradd -g ${USERNAME} ${USERNAME}
RUN chown -R ${USERNAME}:${USERNAME} ${WORKING_DIR}
RUN chmod -R u=rwx,g=rwx ${WORKING_DIR}

USER ${USERNAME}

ENV PATH "$PATH:/home/${USERNAME}/.local/bin"

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 5000

RUN chmod +x service_entrypoint.sh

ENV FLASK_APP=pdqs/app.py

CMD ["flask", "run", "--host", "0.0.0.0"]


