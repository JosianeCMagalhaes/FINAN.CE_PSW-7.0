from django.contrib import messages
from django.contrib.messages import constants
from django.shortcuts import render, redirect
from .models import Conta,Categoria
from .utills import calcula_total, calcula_equilibrio_financeiro,total_conta_vencida_e_proxima
from django.db.models import Sum
from extrato.models import Valores   
from datetime import datetime
# Create your views here.

def home(request):
    valores = Valores.objects.filter(data__month=datetime.now().month)
    entradas = valores.filter(tipo='E')
    saidas = valores.filter(tipo='S')
    contas = Conta.objects.all()
    total_entradas = calcula_total(entradas, 'valor')
    total_saidas = calcula_total(saidas, 'valor')
    saldo_total = calcula_total(contas, 'valor')
    percentual_gastos_essenciais, percentual_gastos_nao_essenciais = calcula_equilibrio_financeiro()
    total_contas_vencidas, total_proximas_do_vencimento = total_conta_vencida_e_proxima()
    
    return render(request, 'home.html', {'contas': contas, 
                                         'saldo_total': saldo_total,
                                         'total_entradas':total_entradas,
                                         'total_saidas':total_saidas,'percentual_gastos_essenciais':percentual_gastos_essenciais,
                                          'percentual_gastos_nao_essenciais':percentual_gastos_nao_essenciais,
                                          'total_contas_vencidas':total_contas_vencidas,
                                          'total_proximas_do_vencimento':total_proximas_do_vencimento ,}) 



def gerenciar(request):
    contas = Conta.objects.all()
    categorias = Categoria.objects.all()
    total_contas = contas.aggregate(Sum('valor'))['valor__sum']
    if not total_contas:
        total_contas = 0
    return render(request, 'gerenciar.html', {'contas': contas,"total_contas":total_contas, 'categorias': categorias})


def cadastrar_banco(request):
    apelido = request.POST.get('apelido')
    banco = request.POST.get('banco')
    tipo = request.POST.get('tipo')
    valor = request.POST.get('valor')
    icone = request.FILES.get('icone')
    
    
    if len(apelido.strip()) == 0 or len(valor.strip()) == 0:
        messages.add_message(request, constants.ERROR, 'Preencha todos os campos')
        return redirect('/perfil/gerenciar/')
    
    if not icone:
        messages.add_message(request, constants.ERROR, 'Selecione uma Ícone')
        return redirect('/perfil/gerenciar/')
    
    conta = Conta(
        apelido = apelido,
        banco=banco,
        tipo=tipo,
        valor=valor,
        icone=icone
    )

    conta.save()

    messages.add_message(request, constants.SUCCESS, 'Conta cadastrada com sucesso')
    return redirect('/perfil/gerenciar/')


def deletar_banco(request, id):
    conta = Conta.objects.get(id=id)
    conta.delete()
    
    messages.add_message(request, constants.SUCCESS, 'Conta removida com sucesso')
    return redirect('/perfil/gerenciar/')


def cadastrar_categoria(request):
    nome = request.POST.get('categoria')
    essencial = bool(request.POST.get('essencial'))
    print(essencial)
    if len(nome.strip()) == 0:
        messages.add_message(request, constants.ERROR, 'Preencha todos os campos')
        return redirect('/perfil/gerenciar/')
    
    if not isinstance(essencial,bool):
        messages.add_message(request, constants.ERROR, 'valor não acento')
        return redirect('/perfil/gerenciar/')
   
    
        

    categoria = Categoria(
        categoria=nome,
        essencial=essencial
    )
    
    categoria.save()

    messages.add_message(request, constants.SUCCESS, 'Categoria cadastrada com sucesso')
    return redirect('/perfil/gerenciar/')


def update_categoria(request, id):
    categoria = Categoria.objects.get(id=id)

    categoria.essencial = not categoria.essencial

    categoria.save()

    return redirect('/perfil/gerenciar/')

def dashboard(request):
    dados = {}
    categorias = Categoria.objects.all()

    for categoria in categorias:
        total = 0
        valores =  Valores.objects.filter(categoria=categoria)
        for v in valores:
            total += v.valor
            if total == None:
                total = 0
        dados[categoria.categoria] = total
    return render(request, 'dashboard.html', {'labels': list(dados.keys()), 
    'values': list(dados.values())})