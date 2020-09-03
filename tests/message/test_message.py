""" Tests for message module
"""

from styler_rest_framework import message


def test_18_n():
    assert message.get(
        'validation.required_value', 'en') == 'Required field'
    assert message.get(
        'validation.required_value', 'ja') == 'Required field (ja)'
    assert message.get(
        'validation.required_value') == 'Required field (ja)'
    assert message.get(
        'validation.required_value', 'es') == 'Required field (ja)'
