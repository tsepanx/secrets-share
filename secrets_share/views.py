from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse
from django.views import generic

from .models import Message


class IndexView(generic.TemplateView):
    template_name = 'secrets_share/index.html'


# class DetailView(generic.DetailView):
#     model = Message
#     template_name = 'secrets_share/detail.html'


def detail(request, hash_id):
    for m in Message.objects.all():
        if m.get_hash_id() == hash_id:
            return render(request, 'secrets_share/detail.html', context={'message': m})

    raise Http404("No such message")


class SubmitView(generic.CreateView):
    model = Message
    fields = ['title', 'text']
    template_name = 'secrets_share/submit.html'

    def post(self, request, *args, **kwargs):
        try:
            title = request.POST['title']
            text = request.POST['text']

            message = Message(title=title, text=text)
        except Exception as e:
            print(e)

            return render(request, 'secrets_share/submit.html')
        else:
            message.save()
            return HttpResponseRedirect(reverse('secrets_share:detail_hash', args=(message.get_hash_id(),)))
