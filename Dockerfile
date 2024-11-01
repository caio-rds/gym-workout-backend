FROM python:3.12-slim

WORKDIR /code

COPY ./requirements.txt ./requirements.txt

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

COPY ./src ./src/

ENV DATABASE_URL=""
ENV SECRET=""
EXPOSE 8000

ENTRYPOINT ["uvicorn", "src.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8000"]