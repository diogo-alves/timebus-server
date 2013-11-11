from django.conf.urls import patterns, include, url
from webservice.api import *
from webservice.views import get_rota
from tastypie.api import Api

api_v1 = Api(api_name= 'v1')
api_v1.register(LinhaResource())
api_v1.register(ViaResource())
api_v1.register(ItinerarioResource())
api_v1.register(PontoResource())
api_v1.register(HorarioResource())


urlpatterns = patterns('',

    url(r'^', include(api_v1.urls)),
    url(r'^v1/rotas/linha/(?P<id>\d+)', get_rota)

)
