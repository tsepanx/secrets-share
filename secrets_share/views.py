from django.views import generic

from .models import Message


class IndexView(generic.TemplateView):
    template_name = 'secrets_share/index.html'


class DetailView(generic.DetailView):
    model = Message
    template_name = 'secrets_share/detail.html'
