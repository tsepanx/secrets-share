from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse
from django.views import generic

from .models import Message
from . import encryption


def get_message_by_hash_id(hash_id):
    for m in Message.objects.all():
        if m.get_hash_id() == hash_id:
            return m

    return None


class IndexView(generic.TemplateView):
    template_name = 'secrets_share/index.html'


def detail(request, hash_id):
    message = get_message_by_hash_id(hash_id)

    if not message:
        raise Http404('No such Message')

    context = {'message': message}

    if request.method == 'GET':
        return render(request, 'secrets_share/detail.html', context)

    elif request.method == 'POST':
        password = request.POST['password']

        decrypted_text = encryption.decrypt(message.text, password)

        if not decrypted_text:
            context['error_message'] = 'Wrong password'
            return render(request, 'secrets_share/detail.html', context)

        context['decrypted_text'] = decrypted_text
        return render(request, 'secrets_share/detail.html', context)


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
            password = request.POST['password']
            message.save(password=password)
            return HttpResponseRedirect(reverse('secrets_share:detail_hash', args=(message.get_hash_id(),)))
