from django.test import TestCase
from django.template import Template, Context


class TestTT(TestCase):

    def test_rendered(self):
        template_to_render = Template(
            "{% load livewire_tags %}"
            "{% livewire_scripts %}"
        )
        rendered_template = template_to_render.render(Context())
        self.assertTrue("window.livewire" in rendered_template)
