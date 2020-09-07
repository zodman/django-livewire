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
import logging
import xml.etree.ElementTree as ET
from .utils import get_id, get_component_name, instance_class
from .utils import get_vars, snakecase

log = logging.getLogger(__name__)


def livewire_message(request, component_name):
    inst = instance_class(component_name)
    context = {}
    if request.method == "POST":
        context = inst.parser_payload(request)
    resp = inst.render(**context)
    return JsonResponse(resp, safe=False)


class LivewireTemplateTag:
    def render_to_templatetag(self, **kwargs):
        self.id = get_id()
        component = self.get_component_name()
        data = self.get_data()
        initial_data = {
            "id": self.id,
            "name": component,
            "redirectTo": False,
            "events": [],  # TODO: 
            "eventQueue": [], # TODO:
            "dispatchQueue": [], # TODO
            "data": data,
            "children": {},   # TODO:
            "effects": [],   # TODO:
            "checksum": "9e4c194bb6aabf5f1",  # TODO: checksum
        }
        context = self.get_context_data(**kwargs)
        context["initial_data"] = initial_data
        return self.render_component(**context)

class LivewireProcessData:

    def fill(self, context):  # Livewire Compatility https://laravel-livewire.com/docs/properties
        self.update_context(context)

    def update_context(self, data_context):
        for key, value in data_context.items():
            setattr(self, key, value)
        context = self.get_context_data()
        if data_context:
            context.update(data_context)
        return context

    def parser_payload(self, request):
        self.request = request
        payload = json.loads(request.body)
        self.id = payload.get("id")
        data = payload.get("data", {})
        action_queue = payload.get("actionQueue", [])
        for action in action_queue:
            action_type = action.get("type")
            action_payload = action.get("payload")
            if action_type == "callMethod":
                self.update_context(payload.get("data"))
                method = action_payload.get("method")
                params = action_payload.get("params", [])
                """
                TODO:
                    RUN THIS IT IS REALLY SAFE ???
                    https://www.toptal.com/python/python-design-patterns
                    patterns
                """
                local_method = getattr(self, method)
                return local_method(*params)
            elif action_type == "syncInput":
                data[action_payload["name"]] = action_payload["value"]
                return self.update_context(data)



class LivewireComponent(LivewireTemplateTag, LivewireProcessData):
    id = None
    template_name = None

    def get_component_name(self):
        name = self.__class__.__name__.replace("Livewire", "")
        name = snakecase(name)
        return name

    def get_template_name(self):
        if self.template_name:
            return self.template_name
        raise Exception("not template name set")  # 

    def get_data(self):
        mount_result = {}
        # call mount if exists
        if hasattr(self, "mount") and callable(self.mount):  # Livewire Compatility
            mount_result = self.mount()
        params = get_vars(self)
        for property in params:
            mount_result[property] = getattr(self, property)
        return mount_result

    def get_context_data(self, **kwargs):
        return kwargs

    def get_dom(self, template_name, context):
        context = self.get_context_data(**context)
        return self.render_component(template_name, context)

    def render(self, **context):
        """
            A Livewire component's render method gets called on the initial page load AND every subsequent component update.
            TODO: to Implement
        """
        template_name = self.get_template_name()
        return self.view(template_name, context)

    def view(self, template_name, context):
        dom = self.get_dom(template_name, context)
        return self.render_to_response(template_name, dom)

    def render_component(self, **context):
        component_template = self.get_template_name()
        data = self.get_data()
        initial_data = context.get("initial_data")
        if initial_data:
            del context["initial_data"]
        context.update(data)
        component_render = render_to_string(
            component_template, context=context
        )
        root = htmlement.fromstring(component_render).find("div")
        root.set("wire:id", self.id)
        if initial_data:
            root.set("wire:initial-data", json.dumps(initial_data))
        res = ET.tostring(root)
        return mark_safe(smart_str(res))

    def render_to_response(self,  template_name, dom):  # TODO: chnge to use render method on component view
        json_response = {
            "id": self.id,
            "name": self.get_component_name(),
            "dom": dom,
            "fromPrefetch": "",
            "redirectTo": "",
            "children": [],
            "dirtyInputs": [],
            "data": self.get_data(),
            "eventQueue": [],
            "dispatchQueue": [],
            "events": [],
            "events":[],
            "checksum": "c24",
        }
        if hasattr(self, "updates_query_string"):
            json_response.update({'updatesQueryString': self.updates_query_string})
        return json_response
