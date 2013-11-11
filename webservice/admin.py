#! -*- coding:utf-8 -*-

__author__ = 'Diogo Alves'

from django.contrib import admin
from webservice.models import *
from webservice.forms import EmpresaForm

class EmpresaAdmin(admin.ModelAdmin):
    form = EmpresaForm
    list_display = ('nome', 'endereco', 'telefone', 'site',)
    list_display_links = list_display
    search_fields = ('nome',)
    list_per_page = 20


class LinhaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'empresa',)
    list_display_links = list_display
    search_fields = ('id', 'nome', 'empresa__nome',)
    list_per_page = 20


class PontoAdmin(admin.ModelAdmin):
    list_display = ('id', 'endereco', 'bairro', 'modificado_em')
    list_display_links = list_display
    search_fields = ('id', 'endereco',)
    list_per_page = 20
    filter_horizontal = ('linhas',)

class PontoMapeadoAdmin(admin.ModelAdmin):

    list_filter = ('verificado',)
    list_display = ('id', 'endereco', 'bairro', 'verificado')
    list_display_links = list_display
    search_fields = ('id', 'endereco', 'bairro')
    list_per_page = 20

    actions = ('confirmar_pontos',)

    def confirmar_pontos(self, request, queryset):
        """
        Confirma as informações dos pontos mapeados, adicionando-os ao sistema.
        """

        queryset.update(verificado=True)
        if len(queryset) == 1:
            self.message_user(request, "O ponto selecionado foi adicionado ao sistema!")
        else:
            self.message_user(request, "Os pontos selecionados foram adicionados ao sistema!")

    confirmar_pontos.short_description = 'Adicionar pontos selecionados ao sistema'


class HorarioAdmin(admin.ModelAdmin):
    list_filter = ('tipo_dia', 'linha',)
    list_display = ('linha', 'hora' , 'tipo_dia',)
    list_display_links = list_display
    search_fields = ('linha__nome', 'linha__id',)
    list_per_page = 20


class ViaAdmin(admin.ModelAdmin):
    list_display = ('endereco',)
    search_fields = ('endereco',)
    list_per_page = 20


class ItinerarioAdmin(admin.ModelAdmin):
    list_filter = ('linha',)
    list_display = ('linha', 'sentido', 'sequencia', 'via',)
    list_display_links = list_display
    search_fields = ('linha__nome', 'via__endereco',)
    list_per_page = 20


class RotaAdmin(admin.ModelAdmin):
    list_filter = ('linha',)
    list_display = ('linha', 'arquivo')
    list_display_links =  list_display
    search_fields = ('linha__nome',)
    list_per_page = 20


admin.site.register(Empresa, EmpresaAdmin)
admin.site.register(Linha, LinhaAdmin)
admin.site.register(Ponto, PontoAdmin)
admin.site.register(PontoMapeado, PontoMapeadoAdmin)
admin.site.register(Horario, HorarioAdmin)
admin.site.register(Via, ViaAdmin)
admin.site.register(Itinerario, ItinerarioAdmin)
admin.site.register(Rota, RotaAdmin)

