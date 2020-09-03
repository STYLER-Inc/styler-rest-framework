""" Tests for validation module
"""

from styler_rest_framework.validation import I18nValidatorMixin
from styler_rest_framework.validation import validators as va


class MyModel(I18nValidatorMixin):
    validates = [
        ('name', va.is_required()),
        ('age', va.is_required(), va.is_less_than_number(100))
    ]


def test_validation():
    model = MyModel()
    model.name = None
    model.age = 200

    result, errors = model.is_valid()

    assert not result
    assert errors == {
        'mymodel.age': '100より小さい値にしてください',
        'mymodel.name': '入力してください'
    }


def test_validation_i18n():
    model = MyModel()
    model.name = None
    model.age = 200

    result, errors = model.is_valid(locale='en')

    assert not result
    assert errors == {
        'mymodel.age': 'Should be less than 100',
        'mymodel.name': 'Required field'
    }


def test_valid():
    model = MyModel()
    model.name = 'John'
    model.age = 67

    result, errors = model.is_valid()

    assert result
    assert errors == {}
