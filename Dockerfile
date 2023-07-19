FROM python:3.8

WORKDIR /discord_interactive_help
COPY . .

RUN pip install discord.py
RUN pip install -e .

CMD ["python", "main.py"]