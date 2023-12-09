FROM python:3.11-slim

WORKDIR /app

COPY ./ /app

ENV HOST=0.0.0.0
ENV LISTEN_PORT 8000
EXPOSE 8000

RUN pip install --no-cache-dir -r requirements.txt


#CMD ["streamlit", "run", "application_streamlit.py","--server.port=80", "--server.address=0.0.0.0"]

CMD ["chainlit", "run", "application_chainlit.py", "-w", "--port=8000", "--host=0.0.0.0"]
