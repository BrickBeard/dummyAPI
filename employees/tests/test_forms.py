from employees.forms import searchForm, create_form, update_form, UserRegisterForm
import pytest


@pytest.mark.parametrize(
    'search_query',
    [('test'),
     ('   test'),
     ('test   '),
     ('12AB{}<>)@/\!`')
     ]
)
def test_search_form(search_query):
    form = searchForm(data={'search_query': search_query})
    assert form.is_valid()
