FROM python:3.9-slim-buster

ENV PYTHONPATH /app
ENV PYTHONBUFFERED 1

RUN mkdir /app
RUN useradd --create-home app
ENV PATH "/home/app/.local/bin:${PATH}"
WORKDIR /app
RUN chown -R app:app /app

USER app

COPY requirements.txt .

RUN pip install -r requirements.txt
RUN pip install gunicorn

COPY alembic alembic
COPY recipe_book recipe_book
COPY alembic.ini .

COPY entrypoint.sh /entrypoint.sh

EXPOSE 5000

ENTRYPOINT [ "/entrypoint.sh" ]

CMD ["gunicorn", "-b", "0.0.0.0:5000", "recipe_book.wsgi:app"]
