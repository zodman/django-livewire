from django import template
from livewire.views import LivewireComponent
register = template.Library()

@register.inclusion_tag("livewire_scripts.html", takes_context=True)
def livewire_scripts(context):
    return context

@register.simple_tag
def livewire(component,**kwargs):
    # TODO: register Components by livewire.register(ComponentLivewire)
    from core.views import CounterLivewire
    livewire_component = CounterLivewire()
    return livewire_component.render_initial()
