from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from django import forms

from .models import Message
from . import encryption


def get_message_by(hash_id):
    for m in Message.objects.all():
        if m.get_hash_id() == hash_id:
            return m

    raise Http404('No such Message')


class IndexView(generic.TemplateView):
    template_name = 'secrets_share/index.html'


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


class SubmitForm(forms.ModelForm):
    title = forms.CharField(label='Message Title')
    text = forms.CharField(widget=forms.Textarea, label='Message Text')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    # burn_after_reading = forms.BooleanField(required=False)

    class Meta:
        model = Message
        fields = ['title', 'text']


class SubmitView(generic.CreateView):
    form_class = SubmitForm
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
