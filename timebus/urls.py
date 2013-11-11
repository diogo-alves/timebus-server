from django.conf.urls import patterns, include, url
from webservice.api import *
from webservice.views import get_rota
from tastypie.api import Api
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

#api_v1 = Api(api_name= 'v1')
#api_v1.register(LinhaResource())
#api_v1.register(ViaResource())
#api_v1.register(ItinerarioResource())
#api_v1.register(PontoResource())
#api_v1.register(HorarioResource())
#api_v1.register(RotaResource())




urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'timebus.views.home', name='home'),
    # url(r'^timebus/', include('timebus.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^api/', include(api_v1.urls)),
    #url(r'^api/v1/rotas/linha/(?P<id>\d+)', get_rota)
    url(r'^api/', include('webservice.urls'))

)
