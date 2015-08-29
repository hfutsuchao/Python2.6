from django.shortcuts import render_to_response
from django.core.mail import send_mail
from django.http import HttpResponseRedirect

def contact(request):
    errors = []
    if request.method == 'POST':
        if not request.POST.get('subject', ''):
            errors.append('Enter a subject.')
        if not request.POST.get('message', ''):
            errors.append('Enter a message.')
        if request.POST.get('email') and '@' not in request.POST['email']:
            errors.append('Enter a valid e-mail address.')
        if not errors:
            send_mail(
                request.POST['subject'],
                request.POST['message'],
                request.POST.get('email', 'noreply@example.com'),
                ['hfutsuchao@gmail.com'],
            )
            return HttpResponseRedirect('/contact/thanks/')
    return render_to_response('contactForm.html', {'errors': errors})