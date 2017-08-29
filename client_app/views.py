from django.views.generic import ListView

from chapter_1.models import Post


class PostListView(ListView):
    queryset = Post.objects.published()
    template_name = 'client_app/post/post_list.html'
