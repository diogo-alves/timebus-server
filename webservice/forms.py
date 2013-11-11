#!-*- coding: utf-8 -*-

__author__ = 'Diogo Alves'

from  django.contrib.localflavor.br.forms import BRPhoneNumberField
from django.forms import  ModelForm
from webservice.models import Empresa


class EmpresaForm(ModelForm):
    telefone = BRPhoneNumberField(label='Telefone', help_text=u'Digite um número válido no formato xx-xxxx-xxxx.')

    class Meta:
        model = Empresa