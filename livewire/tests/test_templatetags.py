from django.test import TestCase
from django.template import Template, Context
from django.template.backends.django import Template as DjangoTemplate
from unittest.mock import patch

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

    @patch('livewire.views.render_to_string')
    def test_rendercontext(self, mock_render_to_string):
        mock_render_to_string.return_value ="<div></div>"
        template_str = Template(
            "{% load livewire_tags %}"
            "{% livewire 'hello_world' %}" 
        )
        rendered_template = template_str.render(Context())
        self.assertTrue("wire:id" in rendered_template)
        self.assertTrue("wire:initial-data" in rendered_template)
        
    def test_rendercontext(self):
        template_str = Template(
            "{% load livewire_tags %}"
            "{% livewire 'hello_world' post_id=1 %}" 
        )
        rendered_template = template_str.render(Context())
        self.assertTrue("> 1 <" in rendered_template)
