"""Setup configuration for django_generic_many_to_many_field."""

from setuptools import setup, find_packages
import os


def read_file(filename):
    """Read a file and return its contents."""
    with open(os.path.join(os.path.dirname(__file__), filename), encoding='utf-8') as f:
        return f.read()


setup(
    name='django-generic-many-to-many-field',
    version='0.1.0',
    description='A Django app providing generic many-to-many field functionality',
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    author='Hussein Naeem',
    author_email='husseinnaeemsec@users.noreply.github.com',
    url='https://github.com/husseinnaeemsec/django_generic_many_to_many_field',
    project_urls={
        'Bug Reports': 'https://github.com/husseinnaeemsec/django_generic_many_to_many_field/issues',
        'Source': 'https://github.com/husseinnaeemsec/django_generic_many_to_many_field',
    },
    packages=find_packages(exclude=['tests', 'tests.*']),
    include_package_data=True,
    python_requires='>=3.8',
    install_requires=[
        'Django>=3.2',
    ],
    extras_require={
        'dev': [
            'pytest>=7.0',
            'pytest-django>=4.5',
            'black>=22.0',
            'flake8>=4.0',
            'isort>=5.10',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 3.2',
        'Framework :: Django :: 4.0',
        'Framework :: Django :: 4.1',
        'Framework :: Django :: 4.2',
        'Framework :: Django :: 5.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='django field generic many-to-many contenttype',
    license='MIT',
    zip_safe=False,
)
