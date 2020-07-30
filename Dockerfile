FROM python:2.7-slim-jessie

RUN apt-get update && apt-get install -y libsodium-dev git libevent-dev libzmq-dev libffi-dev libssl-dev gcc file git
WORKDIR /opt/bridge
COPY . /opt/bridge
RUN pip install --upgrade pip==20.1.1 && pip install -r requirements-dev.txt
RUN pip install -e .
RUN git clone --depth 1  https://github.com/openprocurement/templates.regisrty.git /opt/bridge/template_registry && rm -fr /opt/bridge/template_registry/.git
RUN apt-get clean

ENV TZ=Europe/Kiev
ENV LANG="en_US.UTF-8"
ENV LC_ALL="en_US.UTF-8"
ENV LC_LANG="en_US.UTF-8"
ENV PYTHONIOENCODING="UTF-8"
ENV PYTHONPATH="/opt/bridge/:${PYTHONPATH}"

CMD ["/usr/local/bin/databridge", "/etc/templatesregistry_data_bridge.yaml"]
