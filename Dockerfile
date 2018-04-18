FROM troyfontaine/armhf-alpinelinux:3.3
RUN apk add --no-cache  --update\
	nginx uwsgi uwsgi-python py-pip \
	&& pip2 install --upgrade pip \
	&& pip2 install flask

ENTRYPOINT ["/bin/sh"]
