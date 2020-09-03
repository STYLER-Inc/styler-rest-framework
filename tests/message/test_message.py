""" Tests for message module
"""

from styler_rest_framework import message


def test_18_n():
    assert message.get(
        'validation.required_value', 'en') == 'Required field'
    assert message.get(
        'validation.required_value', 'ja') == '入力してください'
    assert message.get(
        'validation.required_value') == '入力してください'
    assert message.get(
        'validation.required_value', 'es') == '入力してください'
