# Django Generic Many-to-Many Field

A Django app that provides generic many-to-many field functionality using Django's ContentType framework. This allows you to create many-to-many relationships between any models without creating explicit through tables for each relationship.

## Features

- Generic many-to-many relationships between any Django models
- Built on Django's ContentType framework
- Django admin integration
- Support for Django 3.2+
- Python 3.8+ compatible

## Installation

You can install django-generic-many-to-many-field via pip:

```bash
pip install django-generic-many-to-many-field
```

## Quick Start

1. Add `django_generic_many_to_many_field` to your `INSTALLED_APPS` setting:

```python
INSTALLED_APPS = [
    ...
    'django.contrib.contenttypes',
    'django_generic_many_to_many_field',
    ...
]
```

2. Run migrations to create the necessary database tables:

```bash
python manage.py migrate django_generic_many_to_many_field
```

## Usage

### Basic Usage

Use the `GenericManyToManyField` in your models:

```python
from django.db import models
from django_generic_many_to_many_field.fields import GenericManyToManyField

class MyModel(models.Model):
    name = models.CharField(max_length=100)
    related_items = GenericManyToManyField()
```

### Working with Relations

The `GenericManyToManyRelation` model stores the actual relationships:

```python
from django_generic_many_to_many_field.models import GenericManyToManyRelation
from django.contrib.contenttypes.models import ContentType

# Create a relationship
relation = GenericManyToManyRelation.objects.create(
    content_type_from=ContentType.objects.get_for_model(source_obj),
    object_id_from=source_obj.id,
    content_type_to=ContentType.objects.get_for_model(target_obj),
    object_id_to=target_obj.id,
)
```

## Development

### Setting Up Development Environment

1. Clone the repository:

```bash
git clone https://github.com/husseinnaeemsec/django_generic_many_to_many_field.git
cd django_generic_many_to_many_field
```

2. Install development dependencies:

```bash
pip install -r requirements-dev.txt
```

3. Run tests:

```bash
pytest
```

### Building and Publishing

To build the package:

```bash
python -m build
```

To publish to PyPI:

```bash
twine upload dist/*
```

## Requirements

- Python >= 3.8
- Django >= 3.2

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Hussein Naeem

## Links

- GitHub: https://github.com/husseinnaeemsec/django_generic_many_to_many_field
- PyPI: https://pypi.org/project/django-generic-many-to-many-field/
- Issue Tracker: https://github.com/husseinnaeemsec/django_generic_many_to_many_field/issues