from django.urls import reverse
import pytest
import json
from tests.factories import TodoFactory


class TestTodoList:
    @pytest.mark.django_db(transaction=True)
    def test_get_todos(self, api_client):
        data = {
            'text': 'test',
            'category': {
                'name': 'test'
            }
        }
        f_1 = TodoFactory.create(**data)
        f_2 = TodoFactory.create(**data)
        f_3 = TodoFactory.create(**data)
        f_4 = TodoFactory.create(**data)
        url = reverse('todo-list')
        response = api_client.get(url)
        assert response.status_code == 200
        assert len(response.data) == 4

    @pytest.mark.django_db(transaction=True)
    def test_todo_filter_by_category(self, api_client):
        data_1 = {
            'text': 'test',
            'category': {
                'name': 'shoes'
            }
        }
        data_2 = {
            'text': 'test',
            'category': {
                'name': 'newcategory'
            }
        }
        f_1 = TodoFactory.create(**data_1)
        f_2 = TodoFactory.create(**data_1)
        f_3 = TodoFactory.create(**data_1)
        f_4 = TodoFactory.create(**data_1)
        f_5 = TodoFactory.create(**data_2)
        url = reverse('todo-list') + "?category_id={0}".format(f_5.category.id)
        response = api_client.get(url)
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]['id'] == f_5.id
        print(response.data[0]['id'])

    @pytest.mark.django_db(transaction=True)
    def test_todo_incorrect_string_filter(self, api_client):
        data_1 = {
            'text': 'test',
            'category': {
                'name': 'shoes'
            }
        }
        data_2 = {
            'text': 'test',
            'category': {
                'name': 'newcategory'
            }
        }
        f_1 = TodoFactory.create(**data_1)
        f_2 = TodoFactory.create(**data_1)
        f_3 = TodoFactory.create(**data_1)
        f_4 = TodoFactory.create(**data_1)
        f_5 = TodoFactory.create(**data_2)
        url = reverse('todo-list') + "?category_id={0}".format('dsad')
        response = api_client.get(url)
        assert response.status_code == 400

    @pytest.mark.django_db(transaction=True)
    def test_todo_filter_with_unexist_category_id(self, api_client):
        data_1 = {
            'text': 'test',
            'category': {
                'name': 'shoes'
            }
        }
        data_2 = {
            'text': 'test',
            'category': {
                'name': 'newcategory'
            }
        }
        f_1 = TodoFactory.create(**data_1)
        f_2 = TodoFactory.create(**data_1)
        f_3 = TodoFactory.create(**data_1)
        f_4 = TodoFactory.create(**data_1)
        f_5 = TodoFactory.create(**data_2)
        url = reverse('todo-list') + "?category_id={0}".format(10**4)
        response = api_client.get(url)
        assert response.status_code == 200
        assert len(response.data) == 0

    @pytest.mark.django_db(transaction=True)
    def test_create_todo(self, api_client):
        data = {
            'text': 'test',
            'category': {
                'name': 'test'
            }
        }
        url = reverse('todo-list')
        response = api_client.post(url, json.dumps(data), content_type='application/json')
        assert response.status_code == 201
        assert response.data['text'] == data['text']


class TestTodoDetail:
    @pytest.mark.django_db(transaction=True)
    def test_get_todo(self, api_client):
        data = {
            'text': 'test',
            'category': {
                'name': 'test'
            }
        }
        f = TodoFactory.create(**data)
        url = reverse('todo-detail', kwargs={'pk': f.id})
        response = api_client.get(url)
        assert response.status_code == 200
        assert response.data['id'] == f.id
        assert response.data['text'] == f.text

    @pytest.mark.django_db(transaction=True)
    def test_get_unexist_todo(self, api_client):
        url = reverse('todo-detail', kwargs={'pk': 10**4})
        response = api_client.get(url)
        assert response.status_code == 404

    @pytest.mark.django_db(transaction=True)
    def test_update_todo(self, api_client):
        data = {
            'text': 'test',
            'category': {
                'name': 'test'
            }
        }
        f = TodoFactory.create(**data)
        new_data = {
            'id': f.id,
            'text': 'updated',
            'category': {
                'name': 'updated'
            }
        }
        url = reverse('todo-detail', kwargs={'pk': f.id})
        response = api_client.put(url, json.dumps(new_data), content_type='application/json')
        assert response.status_code == 200
        assert response.data['id'] == f.id
        assert response.data['text'] == new_data['text']
        assert response.data['category']['name'] == new_data['category']['name']

    @pytest.mark.django_db(transaction=True)
    def test_delete_todo(self, api_client):
        data = {
            'text': 'test',
            'category': {
                'name': 'test'
            }
        }
        f = TodoFactory.create(**data)
        url = reverse('todo-detail', kwargs={'pk': f.id})
        response = api_client.delete(url)
        assert response.status_code == 204
