FROM python:3.11.11-slim

COPY ./src/production_agents/DQN/requirements.txt /app/requirements.txt
COPY ./src/production_agents/DQN/agent_server_DQN.py /app/agent_server_DQN.py
COPY ./src/production_agents/DQN/production_agent_DQN.py /app/production_agent_DQN.py
COPY ./RL4CC /app/RL4CC
COPY ./src /app/src
COPY ./src/production_agents/DQN/configuration_files/checkpoints/trained_checkpoint/ /app/trained_checkpoint/
COPY ./src/production_agents/DQN/configuration_files/agents_parameters.json /app/agents_parameters.json

WORKDIR /app

RUN pip3 install -r requirements.txt
RUN cd RL4CC && pip3 install .

RUN mkdir /home/tesista && \
  useradd -u 1122 tesista && \
  chown tesista:tesista /home/tesista
USER tesista

ENTRYPOINT exec python3 -m flask --app agent_server_DQN run --host=0.0.0.0 --port=5000