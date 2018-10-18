from django.test import RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User, AnonymousUser
from employees.views import index, AllEmployees, FilteredEmployees, createForm, updateForm, deleteEmployee, register
from employees.forms import searchForm, update_form, create_form
from mixer.backend.django import mixer
import pytest
import requests


@pytest.mark.django_db
class TestViews:

    # --------------- index View ---------------
    def test_index_view(self):
        path = reverse('index')
        request = RequestFactory().get(path)
        request.user = AnonymousUser()

        response = index(request)
        assert response.status_code == 200

    def test_index_view_authenticated(self):
        path = reverse('index')
        request = RequestFactory().get(path)
        request.user = mixer.blend(User)

        response = index(request)
        assert response.status_code == 200

    # --------------- AllEmployees View ---------------
    def test_allemployees_view(self):
        path = reverse('all')
        request = RequestFactory().get(path)
        request.user = AnonymousUser()

        response = AllEmployees.as_view()(request)
        assert response.status_code == 200

    def test_allemployees_view_authenticated(self):
        path = reverse('all')
        request = RequestFactory().get(path)
        request.user = mixer.blend(User)

        response = AllEmployees.as_view()(request)
        assert response.status_code == 200

    # --------------- FilteredEmployees View ---------------
    def test_filteredemployees_salary_view(self):
        path = reverse('filtered', kwargs={'filter_by': 'salary'})
        request = RequestFactory().get(path)
        request.user = AnonymousUser()

        response = FilteredEmployees.as_view()(request, filter_by='salary')
        assert response.status_code == 200

    def test_filteredemployees_salary_view_authenticated(self):
        path = reverse('filtered', kwargs={'filter_by': 'salary'})
        request = RequestFactory().get(path)
        request.user = mixer.blend(User)

        response = FilteredEmployees.as_view()(request, filter_by='salary')
        assert response.status_code == 200

    def test_filteredemployees_age_view(self):
        path = reverse('filtered', kwargs={'filter_by': 'age'})
        request = RequestFactory().get(path)
        request.user = AnonymousUser()

        response = FilteredEmployees.as_view()(request, filter_by='age')
        assert response.status_code == 200

    def test_filteredemployees_age_view_authenticated(self):
        path = reverse('filtered', kwargs={'filter_by': 'age'})
        request = RequestFactory().get(path)
        request.user = mixer.blend(User)

        response = FilteredEmployees.as_view()(request, filter_by='age')
        assert response.status_code == 200

    def test_filteredemployees_name_view(self):
        path = reverse('filtered', kwargs={'filter_by': 'name'})
        request = RequestFactory().get(path)
        request.user = AnonymousUser()

        response = FilteredEmployees.as_view()(request, filter_by='name')
        assert response.status_code == 200

    def test_filteredemployees_name_view_authenticated(self):
        path = reverse('filtered', kwargs={'filter_by': 'name'})
        request = RequestFactory().get(path)
        request.user = mixer.blend(User)

        response = FilteredEmployees.as_view()(request, filter_by='name')
        assert response.status_code == 200

    # --------------- createForm View ---------------
    def test_createform_view(self):
        path = reverse('create')
        request = RequestFactory().get(path)
        request.user = AnonymousUser()

        response = createForm(request)
        assert '/login/' in response.url

    def test_createform_view_authenticated(self):
        path = reverse('create')
        request = RequestFactory().get(path)
        request.user = mixer.blend(User)

        response = createForm(request)
        assert response.status_code == 200

    def test_createform_view_post_authenticated(self):
        data = {'csrfmiddlewaretoken': ['hnzAK4nto9i8lEBwSp9dkSedq7OIKGQHIcJA3bUUtZYIFaPfrnRrPxN2Ui1hH2oe'], 'name': [
            'pytest'], 'age': ['111'], 'salary': ['12345']}
        path = reverse('create')
        request = RequestFactory().post(path, data)
        request.user = mixer.blend(User)

        response = createForm(request)
        assert '/update/' in response.url

    # --------------- deleteEmployee View ---------------

    def test_deleteEmployee_view(self):
        path = reverse('delete', kwargs={'id': '1'})
        request = RequestFactory().get(path)
        request.user = AnonymousUser()

        response = deleteEmployee(request, id='1')
        assert '/login/' in response.url

    def test_deleteEmployee_view_authenticated(self):
        url_all = 'http://dummy.restapiexample.com/api/v1/employees'
        employees = requests.get(url_all).json()
        employee_id = employees[-1]['id']
        path = reverse('delete', kwargs={'id': employee_id})
        request = RequestFactory().get(path)
        request.user = mixer.blend(User)

        response = deleteEmployee(request, id=employee_id)
        assert response.url == '/'

    # --------------- updateForm View ---------------

    def test_updateform_view(self):
        path = reverse('update', kwargs={'id': '1'})
        request = RequestFactory().get(path)
        request.user = AnonymousUser()

        response = updateForm(request, id='1')
        assert '/login/' in response.url

    def test_updateform_view_authenticated(self):
        url_all = 'http://dummy.restapiexample.com/api/v1/employees'
        employees = requests.get(url_all).json()
        employee_id = employees[0]['id']
        path = reverse('update', kwargs={'id': employee_id})
        request = RequestFactory().get(path)
        request.user = mixer.blend(User)

        response = updateForm(request, id=employee_id)
        assert response.status_code == 200

    def test_updateform_nonexist_view_authenticated(self):
        url_all = 'http://dummy.restapiexample.com/api/v1/employees'
        employees = requests.get(url_all).json()
        employee_id = int(employees[0]['id'])-1
        path = reverse('update', kwargs={'id': employee_id})
        request = RequestFactory().get(path)
        request.user = mixer.blend(User)

        response = updateForm(request, id=employee_id)
        assert response.url == '/'

    def test_updateform_view_post_authenticated(self):
        url_all = 'http://dummy.restapiexample.com/api/v1/employees'
        employees = requests.get(url_all).json()
        employee_id = employees[0]['id']
        data = {'csrfmiddlewaretoken': ['bUx1U1ymyRBdmSuaBTphToowb58owRPCk0Vd0lp2dxifcDhCCvT2Ka33TJjeq56O'], 'name': [
            'pytest'], 'age': [''], 'salary': ['']}
        path = reverse('update', kwargs={'id': employee_id})
        request = RequestFactory().post(path, data)
        request.user = mixer.blend(User)

        response = updateForm(request, id=employee_id)
        assert response.status_code == 200

    # --------------- register View ---------------

    def test_register_view(self):
        path = reverse('register')
        request = RequestFactory().get(path)
        request.user = AnonymousUser()

        response = register(request)
        assert response.status_code == 200

    def test_register_view_authenticated(self):
        path = reverse('register')
        request = RequestFactory().get(path)
        request.user = mixer.blend(User)

        response = register(request)
        assert response.url == '/'
