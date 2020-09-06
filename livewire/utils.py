from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.encoding import smart_str
from django.utils.safestring import mark_safe
from django.http import JsonResponse
from django.conf import settings
import random
import string
import importlib
import re

IGNORE = ("id", "template_name", "request")


def get_vars(instance):
    props = set()
    for prop in dir(instance):
        if not callable(getattr(instance, prop)) and \
                    "__" not in prop and \
                    prop not in IGNORE \
                    and not prop.startswith("_LivewireComponent"):
            props.add(prop)
    return props


def get_id():
    return ''.join(random.choice(string.ascii_lowercase) for i in range(20))


def snakecase(name):
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()


def get_component_name(name):
    name = name.replace("_", " ")
    return name.title().replace(" ", "")


def instance_class(component_name, **kwargs):
    path = getattr(settings, "LIVEWIRE_COMPONENTS_PREFIX")
    if not path:
        assert False, "LIVEWIRE_COMPONENTS_PREFIX missing"
    module = importlib.import_module(path)
    class_name = get_component_name(component_name)
    class_livewire = getattr(module, '{}Livewire'.format(class_name))
    inst = class_livewire()
    return inst
