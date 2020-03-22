from django.shortcuts import render
from livewire.views import LivewireComponent


class CounterLivewire(LivewireComponent):
    component_name = "counter"
    count = 2
    def decrement(self, *args):
        self.count -=1

    def increment(self, *args):
        self.count +=1

    def get_context(self):
        return {
            'count': self.count
        }

