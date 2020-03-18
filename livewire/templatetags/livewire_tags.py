from django import template
from django.template.loader import render_to_string
import random
import string
import json

register = template.Library()


@register.inclusion_tag("livewire_scripts.html", takes_context=True)
def livewire_scripts(context):
    return context

@register.inclusion_tag("livewire/component.html")
def livewire(component,**kwargs):
    context =  kwargs.copy()
    context["count"] = 0

    component_render = render_to_string(f'{component}.livewire.html',context=context)
    id = ''.join(random.choice(string.ascii_lowercase) for i in range(20))
    initial_data = {
        'id': id,
        'name': component,
        'redirectTo':"",
        "events": [],
        "eventQueue": [],
        "dispatchQueue": [],
        "data": {
                    "count": 0
                },
        "children": [],
        "checksum": "9e4c194bb6aabf5f152fe4358385b77c396d711ba4886ac5d41513f1eb6527d3"
    }
    context = {
        'livewire': {
            'id': id,
            'initial_data': json.dumps(initial_data)
        },
        'component': component_render
    }
    return context
