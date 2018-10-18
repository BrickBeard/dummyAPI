from django.test import RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from employees.views import index
# from mixer.backend.django import mixer


class TestViews:

    def test_index_view(self):
        path = reverse('index')
        request = RequestFactory().get(path)

        response = index(request)
        assert response.status_code == 200

    def test_index_view_authenticated(self):
        path = reverse('index')
        request = RequestFactory().get(path)

        response = index(request)
        assert response.status_code == 200
