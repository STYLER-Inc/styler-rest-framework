""" Module for validations (i18n enabled)
"""

from styler_rest_framework import message
from styler_validation import ValidatorMixin
from styler_validation import validators  # NOQA


class I18nValidatorMixin(ValidatorMixin):
    """ Translates validation messages
    """
    def is_valid(self, locale='ja', **kwargs):
        result, errors = super().is_valid(**kwargs)
        if result:
            return result, errors
        localized_errors = {}
        for key, msg in errors.items():
            if len(msg) == 2:
                localized_errors[key] = message.get(
                    f'validation.{msg[0]}', locale=locale, value=msg[1])
            else:
                localized_errors[key] = message.get(
                    f'validation.{msg[0]}', locale=locale)
        return result, localized_errors
