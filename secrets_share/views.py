from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse
from django.views import generic

from .forms import SubmitForm
from .models import Message
from . import encryption


def get_message_by(hash_id):
    for m in Message.objects.all():
        if m.get_hash_id() == hash_id:
            return m

    raise Http404('No such Message')


def detail(request, hash_id):
    message = get_message_by(hash_id)

    context = {'message': message}

    if request.method == 'GET':
        return render(request, 'secrets_share/detail.html', context)

    elif request.method == 'POST':
        password = request.POST['password']
        decrypted_text = encryption.decrypt(message.text, password)

        if decrypted_text:
            context['decrypted_text'] = decrypted_text
            return render(request, 'secrets_share/detail.html', context)
        else:
            context['error_message'] = 'Wrong password'
            return render(request, 'secrets_share/detail.html', context)


class SubmitView(generic.CreateView):
    form_class = SubmitForm
    template_name = 'secrets_share/index.html'

    def post(self, request, *args, **kwargs):
        try:
            text = request.POST['text']

            message = Message(text=text)
        except Exception as e:
            raise Http404(e)
        else:
            password = request.POST['password']
            message.save(password=password)

            return HttpResponseRedirect(reverse('secrets_share:detail_hash', args=(message.get_hash_id(),)))
