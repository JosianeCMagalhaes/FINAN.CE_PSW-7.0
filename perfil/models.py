from django.db import models
from datetime import datetime


# Create your models here.
class Categoria(models.Model):
    categoria = models.CharField(max_length=50)
    essencial = models.BooleanField(default=False)
    valor_planejamento = models.FloatField(default=0)

    def __str__(self):
        return self.categoria

    def total_gasto(self):
        from extrato.models import Valores
        valores = Valores.objects.filter(categoria__id=self.id).filter(data__month=datetime.now().month).filter(tipo='S') # noqa
        from .utils import calcula_total
        total_valor = calcula_total(valores, 'valor')

        return total_valor if total_valor else 0

    def total_mes(self):
        from extrato.models import Valores
        valores = Valores.objects.filter(data__month=datetime.now().month).filter(tipo='S') # noqa
        from .utils import calcula_total
        total_ = calcula_total(valores, 'valor')

        return total_ if total_ else 0

    def calcula_percentual_gasto_por_categoria(self):
        # Adicione o try para evitar o ZeroDivisionError (Erro de divisão por zero) # noqa
        try:
            return int((self.total_gasto() * 100) / self.valor_planejamento)
        except: # noqa
            return 0

    def total_mes(self):
        from extrato.models import Valores
        valores = Valores.objects.filter(data__month=datetime.now().month).filter(tipo='S') # noqa
        from .utils import calcula_total
        total = calcula_total(valores, 'valor')

        return total if total else 0


class Conta(models.Model):
    banco_choices = (
        ('NU', 'Nubank'),
        ('CE', 'Caixa Econômica'),
        ('IU', 'Itaú Unibanco'),
        ('IT', 'Iti'),
        ('BB', 'Banco do Brasil'),
        ('BR', 'Bradesco'),
        ('C6', 'C6'),
    )

    tipo_choices = (
        ('PF', 'Pessoa Física'),
        ('PJ', 'Pessoa Jurídica'),
    )

    apelido = models.CharField(max_length=50)
    banco = models.CharField(max_length=2, choices=banco_choices)
    tipo = models.CharField(max_length=2, choices=tipo_choices)
    valor = models.FloatField()
    icone = models.ImageField(upload_to='icones')

    def __str__(self):
        return self.apelido
