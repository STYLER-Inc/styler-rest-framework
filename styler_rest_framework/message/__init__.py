""" Handles i18n
"""

import os

from i18n import t
import i18n


dir_path = os.path.dirname(os.path.realpath(__file__))
i18n.set('enable_memoization', True)
i18n.load_path.append(f'{dir_path}/labels')
i18n.set('locale', 'ja')
i18n.set('fallback', 'ja')


def get(key, locale='ja', **kwargs):  # pragma: no coverage
    return t(key, locale=locale, **kwargs)


def load_path(path):  # pragma: no coverage
    i18n.load_path.append(path)
