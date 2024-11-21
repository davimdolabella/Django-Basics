from django.shortcuts import render
from django.http import HttpResponse
from .models import Pessoa
def ver_produto(request):
    if request.method == "GET":
        return render(request, 'ver_produto.html',{'Nome':'Caio'})
    elif request.method == "POST":
        nome = request.POST.get('nome')
        idade = request.POST.get('idade')
        
        pessoa = Pessoa(nome=nome, idade=idade)
        pessoa.save()
        pessoas = Pessoa.objects.filter(idade=16)

        return HttpResponse(pessoas)
    
