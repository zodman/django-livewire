from django.test import TestCase
from django.template import Template, Context
from .views import LivewireComponent


class CounterLivewire(LivewireComponent):
    pass

class TestTT(TestCase):
    def test_rendered(self):
        template_to_render = Template(
            "{% load livewire_tags %}"
            "{% livewire_styles %}"
            "{% livewire_scripts %}"
        )
        rendered_template = template_to_render.render(Context())
        self.assertTrue("window.livewire" in rendered_template)
        self.assertTrue("wire:loading" in rendered_template)

    def test_rendercontext(self):
        template_str = Template(
            "{% load livewire_tags %}"
            "{% livewire 'counter' %}" 
        )
        rendered_template = template_str.render(Context())
        print(rendered_template)
