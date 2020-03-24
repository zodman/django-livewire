from django.shortcuts import render
from livewire.views import LivewireComponent
from django.db.models import Q
from core.models import Post
import logging

log = logging.getLogger(__name__)


def posts(request):
    context = {
        'posts': list(Post.objects.all().values("id", "title", "content"))
     }
    return render(request, "posts.html", context)


class PostsLivewire(LivewireComponent):

    def mount(self, **kwargs):
        posts = kwargs.get("posts")
        return {
            'posts': posts
        }


class CounterLivewire(LivewireComponent):
    count = 2

    def decrement(self, *args):
        self.count -= 1

    def increment(self, *args):
        self.count += 1


class HelloworldLivewire(LivewireComponent):
    message = "Hellowwwww mundo!"


class HelloworldDatabindLivewire(LivewireComponent):
    message = "Hellowwwww mundo!"


class SearchPostsLivewire(LivewireComponent):
    search = ""

    def mount(self, **kwargs):
        posts = Post.objects.all()
        if self.search:
            print("search:" + self.search)
            posts = posts.filter(Q(title__icontains=self.search) | \
	    		         Q(content__icontains=self.search))
            print("c: {}".format(posts.count()))

        return {
            'posts': list(posts.values("id", "title", "content"))
        }

