from employees.forms import searchForm, create_form, update_form, UserRegisterForm
import pytest

# --------------- Search Form ---------------


@pytest.mark.parametrize(
    'search_query',
    [('test'),
     ('   test'),
     ('test   '),
     ('   test   '),
     (12345),
     ('12AB{}<>)@/!`'),
     ('__--++==')
     ]
)
def test_search_form(search_query):
    form = searchForm(data={'search_query': search_query})
    assert form.is_valid()

# --------------- Create Form ---------------


@pytest.mark.parametrize(
    'name, age, salary',
    [(123, 123, 123),
     ('test', '123', '12345'),
     ('   test', '   123', '   12345'),
     ('test   ', '123   ', '12345   '),
     ('!@#$%^&*()/<>"', '?/`', '<>":}{')]
)
def test_create_form(name, age, salary):
    form = create_form(data={'name': name, 'age': age, 'salary': salary})
    assert form.is_valid()

# --------------- Update Form ---------------


@pytest.mark.parametrize(
    'name, age, salary',
    [(123, 123, 123),
     ('test', '123', '123'),
     ('   test', '   123', '   123'),
     ('test   ', '123   ', '123   '),
     ('!@#$%^&*()/<>"', '///', '////'),
     ('', '', '123'),
     ('', '123', ''),
     ('test', '', '')]
)
def test_update_form(name, age, salary):
    form = update_form(data={'name': name, 'age': age, 'salary': salary})
    assert form.is_valid()

# --------------- Register Form ---------------


@pytest.mark.django_db
@pytest.mark.parametrize(
    'username, first_name, last_name, email, password1, password2',
    [('pytest', '', '', '', '1234five6', '1234five6'),
     ('pytest', 'py', 'test', 'py@te.st', '1234five6', '1234five6'),
     ('123', '123', '123', 'py@te.st', '1234five6', '1234five6'),
     (123, 123, 123, 'py@te.st', '1234five6', '1234five6')]
)
def test_register_form(username, first_name, last_name, email, password1, password2):
    form = UserRegisterForm(data={'username': username, 'first_name': first_name,
                                  'last_name': last_name, 'email': email, 'password1': password1, 'password2': password2})
    assert form.is_valid()
