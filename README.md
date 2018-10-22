# Dummy API App: Test Application for a public rest API

[![Website](https://img.shields.io/badge/website-live-brightgreen.svg?style=flat-square)](https://dummyapi18.herokuapp.com/) [![built-with-Django](https://img.shields.io/badge/Built%20With-Django%202.1.2-orange.svg?style=flat-square)](https://www.djangoproject.com/) [![CSS-Bulma](https://img.shields.io/badge/CSS-Bulma-blue.svg?style=flat-square)](https://bulma.io/)

**dummyAPI** is a test app project to practice consuming and manipulating a public example API: **[Dummy API Example](http://dummy.restapiexample.com/)**.

### Features:

- Search and Sort views for the example employee database
- Authentication system (Register, Log-In, Variable Views)
- CRUD operations
- Django Framework
- Bulma CSS Framework
- Pytest & Coverage testing
- Profile Images from [Random User Generator](https://randomuser.me/)

#### To setup locally:

1. Clone the repo to your local machine
2. `cd dummyAPI`
3. `python3 virtualenv venv` (virtualenv name is variable. Current python version is **3.6.1**)
4. Activate the virtual environment and then: `pip install -r requirements.txt`
5. `python manage.py migrate && python manage.py createsuperuser` (Follow the prompts)
6. And you're good to go! `python manage.py runserver` (Should be running on **localhost:8000**)

---

### Examples

**REGISTRATION**:

![Registration Gif](readme/registration.gif)

---

**AUTHENTICATION DIFFERENCES**:

![Authentication Changes Gif](readme/diff%20users.gif)

---

> This site was made largely to experiment with and understand different aspects of the Django web framework and public API interaction, and thus not all best practices were adhered to. I welcome any input that could help optimize this codebase. Thank you.
