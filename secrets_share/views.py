from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Message


class IndexView(generic.TemplateView):
    template_name = 'secrets_share/index.html'


class DetailView(generic.DetailView):
    model = Message
    template_name = 'secrets_share/detail.html'


class SubmitView(generic.CreateView):
    model = Message
    fields = ['title', 'text']
    template_name = 'secrets_share/submit.html'

    def post(self, request, *args, **kwargs):
        try:
            # selected_choice_id = request.POST['choice']
            title = request.POST['title']
            text = request.POST['text']

            # submit_date = timezone.now()

            message = Message(title=title, text=text)
        except Exception as e:
            print(e)

            context = {
                'error_message': "Please fill all fields"
            }

            return render(request, 'secrets_share/submit.html', context)
        else:
            message.save()
            return HttpResponseRedirect(reverse('secrets_share:detail', args=(message.id,)))


# def submit_message(request):
#     try:
#         # selected_choice_id = request.POST['choice']
#         message = Message(**request.POST)
#     except Exception as e:
#         print(e)
#
#         context = {
#             'error_message': "Please fill all fields"
#         }
#
#         return render(request, 'secrets_share/submit.html', context)
#     else:
#         message.save()
#
#         return HttpResponseRedirect(reverse(
#             'secrets_share:detail', args=(message.id,)
#         ))
