from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.encoding import smart_str
from django.utils.safestring import mark_safe
from django.http import JsonResponse
from django.conf import settings
import random
import string
import json
import importlib
import htmlement
import xml.etree.ElementTree as ET


def get_id():
    return ''.join(random.choice(string.ascii_lowercase) for i in range(20))

def get_component_name(name):
    name = name.replace("_", " ")
    return name.title().replace(" ","")

def instance_class(component_name, **kwargs):
    path = getattr(settings,"LIVEWIRE_COMPONENTS_PREFIX")
    if not path:
        assert False, "LIVEWIRE_COMPONENTS_PREFIX missing"
    module = importlib.import_module(path)
    class_name = get_component_name(component_name)
    class_livewire = getattr(module, '{}Livewire'.format(class_name))
    inst = class_livewire(**kwargs)
    return inst


