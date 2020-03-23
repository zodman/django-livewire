from django.shortcuts import render
from livewire.views import LivewireComponent

from core.models import Post


def posts(request):
    context={
        'posts': list(Post.objects.all().values("id", "title", "content"))
     }
    return render(request, "posts.html", context)

class PostsLivewire(LivewireComponent):

    def mount(self, **kwargs):
        posts = kwargs.get("posts")
        return {
            'posts':posts
        }



class CounterLivewire(LivewireComponent):
    count = 2
    def decrement(self, *args):
        self.count -=1

    def increment(self, *args):
        self.count +=1

   

class HelloworldLivewire(LivewireComponent):
    message = "Hellowwwww mundo!"
    

class HelloworldDatabindLivewire(LivewireComponent):
    message = "Hellowwwww mundo!"


