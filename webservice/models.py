#!-*- coding: utf-8 -*-
from django.db import models
from geoposition.fields import GeopositionField

class Empresa(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    endereco = models.CharField(u'endereço', max_length=100)
    telefone = models.CharField(max_length=12)
    email = models.EmailField(u'E-mail', max_length=100)
    site = models.URLField(max_length=100, blank=True)

    class Meta:
        db_table = "empresa"
        ordering = ('nome',)

    def __unicode__(self):
        return self.nome


class Linha(models.Model):
    id = models.CharField(u'número', max_length=4, primary_key=True, help_text=u'No máximo 4 caracteres.')
    nome = models.CharField(max_length=100, unique=True)
    empresa = models.ForeignKey(Empresa)

    class Meta:
        db_table = "linha"
        ordering = ('nome',)
        verbose_name = u'linha de ônibus'
        verbose_name_plural = u'linhas de ônibus'

    def __unicode__(self):
        return u'%s' % self.nome


class Via(models.Model):
    endereco = models.CharField(u'endereço', unique=True, max_length=100)

    class Meta:
        db_table = "via"

    def __unicode__(self):
        return self.endereco


class Itinerario(models.Model):

    SENTIDOS = (
        (1, 'IDA'),
        (2, 'VOLTA'),
    )

    linha = models.ForeignKey(Linha)
    via = models.ForeignKey(Via)
    sentido = models.IntegerField(choices=SENTIDOS, default=1, max_length=1)
    sequencia = models.IntegerField(u'sequência', max_length=3)

    class Meta:
        db_table = "itinerario"
        ordering = ('linha__nome', 'sentido', 'sequencia')
        unique_together = ( 'sentido', 'linha', 'sequencia')
        verbose_name = u'itinerário'

    def __unicode__(self):
        return u"%s - %s" % (self.linha, self.via)


class ModelPonto(models.Model):
    referencia = models.CharField(u'descrição', max_length=100)
    endereco = models.CharField(u'endereço', max_length=100)
    bairro = models.CharField(max_length=100)
    coordenadas = GeopositionField()

    class Meta:
        abstract = True


class Ponto(ModelPonto):

    linhas = models.ManyToManyField(Linha, help_text='Selecione as linhas que passam neste ponto. ', blank=True)
    modificado_em = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "ponto"
        verbose_name = u'ponto de ônibus'
        verbose_name_plural = u'pontos de ônibus'

    def __unicode__(self):
        return u"%s - %s, %s" %(self.id, self.endereco, self.bairro)


class PontoMapeado(ModelPonto):

    verificado  = models.BooleanField(default=False)#, editable=False)

    class Meta:
        db_table = "ponto_mapeado"
        verbose_name = "ponto mapeado"
        verbose_name_plural = "pontos mapeados"

    def __unicode__(self):
        return u"%s - %s, %s" %(self.id, self.endereco, self.bairro)


class Horario(models.Model):

    DIAS = (
        (1,u'Dia útil'),
        (2, u'Sábado'),
        (3, 'Domingo'),
    )

    linha = models.ForeignKey(Linha)
    tipo_dia = models.IntegerField('tipo de dia', choices=DIAS, default=1)
    hora = models.TimeField()

    class Meta:
        db_table = "horario"
        ordering = ('linha__nome', 'tipo_dia', 'hora')
        unique_together = ('tipo_dia', 'hora', 'linha')
        verbose_name = u'horário'

    def __unicode__(self):
        return u"%s - %s - %s" % (self.linha, self.tipo_dia, self.hora)


class Rota(models.Model):
    linha = models.ForeignKey(Linha)
    arquivo = models.URLField('url', help_text='Link do arquivo KML no google maps.')

    class Meta:
        db_table = "rota"

    def __unicode__(self):
        return u'%s' % self.linha