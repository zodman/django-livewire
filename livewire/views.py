from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.encoding import smart_str
from django.utils.safestring import mark_safe
from django.http import JsonResponse
import random
import string
import json
import importlib
import htmlement
import xml.etree.ElementTree as ET

def livewire_message(request, component_name):
    from core.views import CounterLivewire
    inst = CounterLivewire()
    if request.method == "POST":
        body = json.loads(request.body)
        inst.parser_payload(body)
    return JsonResponse(inst.render(), safe=False)

def get_id():
    return ''.join(random.choice(string.ascii_lowercase) for i in range(20))

class LivewireComponent():
    id = None
    context = {}

    def get_component_name(self):
        return self.component_name.lower()

    def get_context(self, **kwargs):
        self.context.update(kwargs)
        return self.context

    def get_dom(self):
        context = self.get_context()
        return self._render_component(context)

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

    def parser_payload(self, payload):
        self.id = payload.get("id")
        self.context.update(payload.get("data"))
        action_queue = payload.get("actionQueue", [])
        for action in action_queue:
            action_type = action.get("type")
            payload = action.get("payload")
            if action_type == "callMethod":
                method = payload.get("method")
                params = payload.get("params",[])
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
            'redirectTo':"",
            "events": [],
            "eventQueue": [],
            "dispatchQueue": [],
            "data": context, 
            "children": [],
            "checksum": "9e4c194bb6aabf5f1" # TODO: checksum
        }
        return self._render_component(context, initial_data=initial_data)

