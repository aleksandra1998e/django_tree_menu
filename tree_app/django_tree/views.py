from django.shortcuts import render


def menu_view(request, name):
    return render(request, 'page.html')
