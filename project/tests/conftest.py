from django.db import connection
from rest_framework.test import APIClient
import pytest


@pytest.fixture(autouse=True)
def django_db_setup(django_db_blocker):
    with django_db_blocker.unblock():
        with connection.cursor() as c:
            c.execute("""
            Drop table if exists category cascade;
            CREATE TABLE category
            (
                id SERIAL PRIMARY KEY,
                name CHARACTER VARYING(200) NOT null UNIQUE
            );
            Drop table if exists todo cascade;
            CREATE TABLE todo
            (
                id SERIAL PRIMARY KEY,
                text CHARACTER VARYING(200),
                category integer,
                CONSTRAINT fk_category
                  FOREIGN KEY(category)
                  REFERENCES category(id)
                  ON DELETE SET NULL
            );""")


@pytest.fixture
def api_client():
    return APIClient()
