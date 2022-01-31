from django.shortcuts import render

def index(request):
    """ A view to return an index page """
    return render(request, 'home/pages/index.html')