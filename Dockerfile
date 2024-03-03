FROM python:3.12.2-slim-bookworm

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && \
    apt-get -y upgrade && \
    apt-get install -y ffmpeg && \
    pip install -r requirements.txt 

EXPOSE 8501

COPY app/ .

ENTRYPOINT ["streamlit", "run", "--logger.level=debug"]

CMD ["main.py"]