from django.shortcuts import render
from livewire.views import LivewireComponent

def index(request):
    context = {}
    return render(request, "base.html", context)



class CounterLivewire(LivewireComponent):
    component_name = "counter"
    context = {
        'count': 0
    }
    def decrement(self, *args):
        self.context["count"] -=1

    def increment(self, *args):
        self.context["count"]+=1

