from django import template
from livewire.views import LivewireComponent
from livewire.utils import instance_class

register = template.Library()

@register.inclusion_tag("livewire_styles.html", takes_context=True)
def livewire_styles(context):
    return context


@register.inclusion_tag("livewire_scripts.html", takes_context=True)
def livewire_scripts(context):
    return context


@register.simple_tag(takes_context=True)
def livewire(context, component, **kwargs):
    livewire_component = instance_class(component)
    return livewire_component.render_to_templatetag(**kwargs)
