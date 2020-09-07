from django.test import TestCase, override_settings
from django.template import Template, Context
from django.template.backends.django import Template as DjangoTemplate
from unittest.mock import patch
from ..views import LivewireComponent

class RenderViewLivewire(LivewireComponent):
    template_name = "render_view.livewire.html"

    def render(self, **kwargs):
        context = kwargs.copy()
        context["foo"] = 'bar'
        return self.view(context)


@override_settings(LIVEWIRE_COMPONENTS_PREFIX="livewire.tests.test_render")
class RenderTest(TestCase):
    def test_rendermethod(self):
        template_str = Template(
            "{% load livewire_tags %}"
            "{% livewire 'render_view' %}" 
        )
        rendered_template = template_str.render(Context())
        self.assertTrue("bar" in rendered_template)

 
