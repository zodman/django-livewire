from django.test import TestCase, override_settings
from django.template import Template, Context
from django.template.backends.django import Template as DjangoTemplate
from unittest.mock import patch
from ..views import LivewireComponent


class HelloWorldLivewire(LivewireComponent):
    template_name = "hello_world.livewire.html"

class MountLivewire(LivewireComponent):
    template_name = "mount.livewire.html"
    name = "foobar"
    def mount(self):
        self.name = "andres"
        return {'name': self.name}
    
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
        
    @patch("livewire.views.render_to_string") 
    @override_settings(LIVEWIRE_COMPONENTS_PREFIX="livewire.tests.test_templatetags")
    def test_rendercontext(self, mock_render_to_string):
        mock_render_to_string.return_value = Template("<div> {{post_id}} </div>").render(Context({'post_id': 1}))
        template_str = Template(
            "{% load livewire_tags %}"
            "{% livewire 'hello_world' post_id=1 %}" 
        )
        rendered_template = template_str.render(Context())
        self.assertTrue("> 1 <" in rendered_template)
        self.assertTrue("wire:id" in rendered_template)
        self.assertTrue("wire:initial-data" in rendered_template)
        
    @override_settings(LIVEWIRE_COMPONENTS_PREFIX="livewire.tests.test_templatetags")
    def test_mount_method(self):
        template_str = Template(
            "{% load livewire_tags %}"
            "{% livewire 'mount' %}"
        )
        rendered_template = template_str.render(Context())
        self.assertTrue("> andres <" in rendered_template)
 
