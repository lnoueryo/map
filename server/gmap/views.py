from django.shortcuts import render, redirect
def index(reqest):
    return render(reqest, 'index.html')
def redirect_page(reqest):
    return redirect('https://tap-map.jounetsism.biz')