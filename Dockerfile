FROM python:3.9-slim-buster

RUN mkdir /app
RUN groupadd -r recipe_book && useradd -r -s /bin/false -g recipe_book recipe_book
WORKDIR /app
RUN chown -R recipe_book:recipe_book /app

USER recipe_book

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
