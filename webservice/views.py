# encoding: utf-8

from webservice.models import Rota
from webservice.kml_parser import *
from django.shortcuts import HttpResponse

def get_rota(request, id):
    try:
        rota = Rota.objects.get(linha=id)
        lista = get_coordinates_from_kml(rota.arquivo)
        rota_json = coordinates_to_json(lista)
        return HttpResponse(rota_json, content_type="application/json")
    except Exception:
        return HttpResponse('')