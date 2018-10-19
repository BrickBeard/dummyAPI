from django.urls import reverse, resolve
import requests


class TestUrls:

    def test_index_url(self):
        path = reverse('index')
        assert resolve(path).view_name == 'index'

    def test_create_url(self):
        path = reverse('create')
        assert resolve(path).view_name == 'create'

    def test_update_url(self):
        url_all = 'http://dummy.restapiexample.com/api/v1/employees'
        all_employees = requests.get(url_all).json()
        first = all_employees[0]['id']
        path = reverse('update', kwargs={'id': first})
        assert resolve(path).view_name == 'update'

    def test_delete_url(self):
        url_all = 'http://dummy.restapiexample.com/api/v1/employees'
        all_employees = requests.get(url_all).json()
        first = all_employees[-1]['id']
        path = reverse('delete', kwargs={'id': first})
        assert resolve(path).view_name == 'delete'

    def test_employees_url(self):
        path = reverse('all')
        assert resolve(path).view_name == 'all'

    def test_filtered_employees_by_name_url(self):
        path = reverse('filtered', kwargs={'filter_by': 'name'})
        assert resolve(path).view_name == 'filtered'

    def test_filtered_employees_by_age_url(self):
        path = reverse('filtered', kwargs={'filter_by': 'age'})
        assert resolve(path).view_name == 'filtered'

    def test_filtered_employees_by_salary_url(self):
        path = reverse('filtered', kwargs={'filter_by': 'salary'})
        assert resolve(path).view_name == 'filtered'

    def test_registration_url(self):
        path = reverse('register')
        assert resolve(path).view_name == 'register'

    def test_login_url(self):
        path = reverse('login_view')
        assert resolve(path).view_name == 'loginForm'
