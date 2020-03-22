from django import template
from livewire.views import LivewireComponent
from livewire.utils import instance_class
register = template.Library()

@register.inclusion_tag("livewire_scripts.html", takes_context=True)
def livewire_scripts(context):
    return context

@register.simple_tag
def livewire(component,**kwargs):
    livewire_component = instance_class(component, **kwargs)
    return livewire_component.render_initial()
