# Dockerfile
FROM python:3.11

ENV PYTHONUNBUFFERED 1
ENV PYTHONIOENCODING UTF-8

EXPOSE 8501


RUN apt-get update && apt-get install -y \
    build-essential \
    pkg-config \
    python3-dev \
 && rm -rf /var/lib/apt/lists/*

 COPY requirements.txt ./

RUN pip install --upgrade pip && \
    pip install -r requirements.txt


# RUN pip install nltk
# RUN python -m nltk.downloader punkt


COPY . /app/.

RUN ls

ENV PYTHONPATH /app

WORKDIR /app

CMD ["streamlit", "run", "trulens/trulens_eval/trulens_eval/Leaderboard.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.enableCORS", "false", "--server.maxUploadSize", "1024"]

# CMD ["python", "run_starter.py"]




