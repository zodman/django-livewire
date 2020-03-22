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
from .utils import get_id, get_component_name, instance_class

def livewire_message(request, component_name):
    inst = instance_class(component_name)
    if request.method == "POST":
        body = json.loads(request.body)
        inst.parser_payload(body)
    return JsonResponse(inst.render(), safe=False)


class LivewireComponent(object):
    id = None

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def get_component_name(self):
        name = self.__class__.__name__.lower()
        return name.replace("livewire","")

    def get_dom(self):
        context = self.get_context()
        return self._render_component(context)

    def get_context(self):
        kwargs = self.kwargs
        return self.mount(**kwargs)

    def get_response(self):
        dom = self.get_dom()
        return {
            'id': self.id,
            'name': self.get_component_name(),
            'dom': dom,
            'fromPrefetch':'',
            'redirectTo': '',
            'children': [],
            'dirtyInputs': [],
            'data': self.get_context(),
            'eventQueue': [],
            'dispatchQueue': [],
            'events': [],
            'checksum': "c24"
        }

    def update_context(self, data_context):
        context = self.get_context()
        context.update(data_context)
        for key, value in context.items():
            setattr(self, key,value)
        return context


    def parser_payload(self, payload):
        self.id = payload.get("id")
        self.update_context(payload.get("data"))
        action_queue = payload.get("actionQueue", [])
        for action in action_queue:
            action_type = action.get("type")
            payload = action.get("payload")
            if action_type == "callMethod":
                method = payload.get("method")
                params = payload.get("params",[])
                """
                TODO:
                    RUN THIS IT IS REALLY SAFE ???
                    https://www.toptal.com/python/python-design-patterns
                    patterns
                """
                local_method = getattr(self, method)
                local_method(*params)

    def render(self):
        response = self.get_response()
        return response

    def _render_component(self, context, initial_data={} ):
        component_name = self.get_component_name()
        component_render = render_to_string(f'{component_name}.livewire.html',
                                            context=self.get_context())
        root = htmlement.fromstring(component_render).find("div")
        root.set('wire:id', self.id)
        if initial_data:
            root.set("wire:initial-data",json.dumps(initial_data))
        res = ET.tostring(root)
        return  mark_safe(smart_str(res))


    def render_initial(self):
        self.id =  get_id()
        component = self.get_component_name()
        context = self.get_context()
        initial_data = {
            'id': self.id,
            'name': component,
            'redirectTo': False,
            "events": [],
            "eventQueue": [],
            "dispatchQueue": [],
            "data": context, 
            "children": {},
            "checksum": "9e4c194bb6aabf5f1" # TODO: checksum
        }
        return self._render_component(context, initial_data=initial_data)

