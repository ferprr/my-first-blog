from http.client import FORBIDDEN
from webbrowser import get
from .models import Post
from django.shortcuts import redirect, get_object_or_404

FORBIDDEN_URL = '/admin/'
AUTHORS = ['author']

# Builds decorators for access restrictions
def title_required(allowed_titles, fallback=FORBIDDEN_URL):
    def restriction_decorator(function):
        def wrap(request, *args, **kwargs):
            if request.user.title in allowed_titles:
                return function(request, *args, **kwargs)
            else:
                return redirect(fallback)
            
        return wrap

    return restriction_decorator

# Access restriction for editor-only pages
def editor_required(fun):
    return title_required(AUTHORS)(fun)

# Access restriction for post owner pages
def post_owner_required(param):
    def decorator(function):
        def wrap(request, *args, **kwargs):
            author = get_object_or_404(Post, pk=kwargs[param]).author

            if request.user == author:
                return function(request, *args, **kwargs)
            else:
                return redirect('/')
            
        return wrap

    return decorator
