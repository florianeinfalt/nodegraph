FROM conchoid/docker-pyenv:v1.1.5-3-2.7-alpine3.6

RUN pyenv install 2.7.14
RUN pyenv install 3.5.3
RUN pyenv install 3.6.3
RUN pyenv global 2.7.14 3.5.3 3.6.3

RUN pip install setuptools
RUN pip install virtualenv
RUN pip install tox

RUN addgroup -g 116 jenkins
RUN adduser -D -G jenkins -u 112 jenkins root
USER jenkins
