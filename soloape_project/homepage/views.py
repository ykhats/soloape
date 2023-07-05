from django.shortcuts import redirect

# Create your views here.

def index(request):
    template = 'homepage/index.html'
    return redirect('chords_catalog/')

