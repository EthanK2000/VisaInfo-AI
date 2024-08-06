FROM ethankraus/llmware:visainfo

ARG USERNAME=visainfo-ai
ARG USER_UID=1001
ARG USER_GID=$USER_UID
ENV PYTHONPATH=/visainfo-ai

RUN apt-get update \ 
&& apt-get install -y git bash musl-dev

RUN git clone https://github.com/EthanK2000/visainfo-ai.git

# Create the user
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && chown -R $USERNAME:$USER_GID /visainfo-ai

WORKDIR /visainfo-ai

CMD /bin/bash
