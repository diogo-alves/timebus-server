#!-*- coding: utf-8 -*-

__author__ = 'Diogo Alves <diogo.alves.ti@gmail.com>'

from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from webservice.models import *
from tastypie.serializers import Serializer
from tastypie import fields

class LinhaResource(ModelResource):
    class Meta:
        queryset = Linha.objects.all()
        allowed_methods = ['get']
        detail_allowed_methods = ['get']
        resource_name = 'linhas'
        serializer = Serializer(formats = ['json'])
        include_resource_uri = False
        collection_name = 'Linhas'
        max_limit = None
        limit = 0
        filtering = {
            'id': ALL,
            'nome':ALL,
        }

    #altera a saida dos dados
    def dehydrate(self, bundle):
        bundle.data['nome'] = bundle.data['nome'].upper()
        return bundle

    #remove os metadados da resposta
    def alter_list_data_to_serialize(self, request, data_dict):
        return delete_metadata(data_dict)


class ViaResource(ModelResource):
    class Meta:
        queryset = Via.objects.all()
        allowed_methods = ['get']
        detail_allowed_methods = ['get']
        resource_name = 'vias'
        serializer = Serializer(formats = ['json'])
        include_resource_uri = False
        excludes = ['id',]
        collection_name = 'Vias'
        max_limit = None
        limit = 0
        filtering = {
            'id': ALL,
            'endereco': ALL,
            }

    def dehydrate(self, bundle):
        bundle.data['endereco'] = bundle.data['endereco'].upper()
        return bundle

    def alter_list_data_to_serialize(self, request, data_dict):
        return delete_metadata(data_dict)


class ItinerarioResource(ModelResource):
    linha = fields.ForeignKey(LinhaResource, 'linha', full=True)
    via = fields.ForeignKey(ViaResource, 'via', full=True)

    class Meta:
        queryset = Itinerario.objects.all()
        allowed_methods = ['get']
        detail_allowed_methods = ['get']
        resource_name = 'itinerarios'
        serializer = Serializer(formats = ['json'])
        include_resource_uri = False
        excludes = ['id',]
        collection_name = 'Itinerarios'
        max_limit = None
        limit = 0
        filtering = {
            'linha': ALL_WITH_RELATIONS ,
            'via': ALL_WITH_RELATIONS,
        }

    def dehydrate(self, bundle):
        #del bundle.data['linha'] # exclui as informacoes da chave estrangeira (Linha)
        return bundle

    def alter_list_data_to_serialize(self, request, data_dict):
        return delete_metadata(data_dict)


class PontoResource(ModelResource):

    linhas = fields.ToManyField(LinhaResource, 'linhas', full=True)

    class Meta:
        queryset = Ponto.objects.all()
        allowed_methods = ['get']
        detail_allowed_methods = ['get']
        resource_name = 'pontos'
        serializer = Serializer(formats = ['json'])
        include_resource_uri = False
        collection_name = 'Pontos'
        max_limit = None
        limit = 0
        filtering = {
            'endereco': ALL,
            'bairro': ALL,
            'linhas': ALL_WITH_RELATIONS,
            'modificado_em': ALL,
        }

    def dehydrate(self, bundle):
        # subdividindo o campo coordenadas nos campos latitude e longitude
        coord = bundle.data['coordenadas'].split(',')
        bundle.data['latitude'] = coord[0]
        bundle.data['longitude'] = coord[1]
        # juntando os campos endereco e bairro num campo só (endereco)
        bundle.data['endereco'] = bundle.data['endereco'] +', ' + bundle.data['bairro']
        # deletando os campos não mais necessários
        del bundle.data['bairro']
        del bundle.data['coordenadas']
        return bundle

    def hydrate(self, bundle):
        local = bundle.data['endereco'].split(',')
        bundle.data['endereco'] = local[0]
        bundle.data['bairro'] = local[1]
        return bundle

    def alter_list_data_to_serialize(self, request, data_dict):
        return delete_metadata(data_dict)


class PontoMapeadoResource(ModelResource):

    class Meta:
        queryset = PontoMapeado.objects.all()
        allowed_methods = ['post']
        detail_allowed_methods = ['post']
        resource_name = 'pontos-mapeados'
        serializer = Serializer(formats = ['json'])
        include_resource_uri = False
        collection_name = 'Pontos'
        max_limit = None
        limit = 0


    def dehydrate(self, bundle):
        # subdividindo o campo coordenadas nos campos latitude e longitude
        coord = bundle.data['coordenadas'].split(',')
        bundle.data['latitude'] = coord[0]
        bundle.data['longitude'] = coord[1]
        # juntando os campos endereco e bairro num campo só (endereco)
        bundle.data['endereco'] = bundle.data['endereco'] +', ' + bundle.data['bairro']
        # deletando os campos não mais necessários
        del bundle.data['bairro']
        del bundle.data['coordenadas']
        return bundle

    def hydrate(self, bundle):
        #subdividindo o campo endereço em logradouro e bairro
        local = bundle.data['endereco'].split(',')
        del bundle.data['endereco']
        bundle.data['endereco'] = local[0]
        bundle.data['bairro'] = local[1]
        return bundle


    def alter_list_data_to_serialize(self, request, data_dict):
        return delete_metadata(data_dict)

class HorarioResource(ModelResource):
    linha = fields.ForeignKey(LinhaResource, 'linha')

    class Meta:
        queryset = Horario.objects.all()
        allowed_methods = ['get']
        detail_allowed_methods = ['get']
        resource_name = 'horarios'
        serializer = Serializer(formats = ['json'])
        include_resource_uri = False
        collection_name = 'Horarios'
        excludes = ['id', ]
        max_limit = None
        limit = 0
        filtering = {
            'linha': ALL_WITH_RELATIONS ,
            'tipo_dia': ALL ,
        }

    def dehydrate(self, bundle):
        #bundle.data['turno'] = turno(bundle.data['hora'])
        bundle.data['hora'] = bundle.data['hora'].strftime("%H:%M") # formata a hora p/ o formato HH:MM
        del bundle.data['tipo_dia']                                 # exclui o tipo do dia da resposta
        del bundle.data['linha']                                    # exclui as informacoes da chave estrangeira (Linha)
        return bundle

    def alter_list_data_to_serialize(self, request, data_dict):
        return delete_metadata(data_dict)


# class RotaResource(ModelResource):
#     linha = fields.ForeignKey(LinhaResource, 'linha')
#
#     class Meta:
#         queryset = Rota.objects.all()
#         allowed_methods = ['get']
#         detail_allowed_methods = ['get']
#         resource_name = 'rotas'
#         serializer = Serializer(formats = ['json'])
#         include_resource_uri = False
#         collection_name = 'Rotas'
#         excludes = ['id', 'numero']
#         max_limit = None
#         limit = 0
#         filtering = {
#             'linha': ALL_WITH_RELATIONS,
#         }
#
#     def dehydrate(self, bundle):
#         del bundle.data['linha']
#         return bundle
#
#     def alter_list_data_to_serialize(self, request, data_dict):
#         return delete_metadata(data_dict)


# Deleta o dicionario de metadados do json
def delete_metadata(data_dict):
    if isinstance(data_dict, dict):
        if 'meta' in data_dict:
            del(data_dict['meta'])
    return data_dict