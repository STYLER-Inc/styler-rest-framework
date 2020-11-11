#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = [
    'aiohttp',
    'sqlalchemy',
    'pyyaml',
    'psycopg2-binary',
    'sqlalchemy-serializer',
    'styler-identity',
    'styler-middleware',
    'styler-validation',
    'cachetools',
    'certifi',
    'chardet',
    'google-api-core[grpc]',
    'google-auth',
    'google-cloud-core',
    'google-cloud-monitoring',
    'google-cloud-trace >= 0.20.0, < 1.0.0',
    'googleapis-common-protos',
    'grpcio',
    'idna',
    'opencensus-context',
    'opencensus-ext-stackdriver',
    'opencensus',
    'protobuf',
    'pyasn1-modules',
    'pyasn1',
    'pytz',
    'requests',
    'rsa',
    'six',
    'urllib3',
    'google.cloud.logging',
    'python-i18n[YAML]',
    'alembic',
]

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3', ]

setup(
    author="Bruno Toshio Sugano",
    author_email='brunotoshio@gmail.com',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
    ],
    description="Standards used in REST services",
    install_requires=requirements,
    license="MIT license",
    long_description=readme,
    include_package_data=True,
    keywords='styler_rest_framework',
    name='styler_rest_framework',
    packages=find_packages(include=['styler_rest_framework', 'styler_rest_framework.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/STYLER-Inc/styler-rest-framework',
    version='0.11.1',
    zip_safe=False,
)
