# encoding:utf-8

__author__ = 'Diogo Alves <diogo.alves.ti@gmail.com>'

from urllib2 import urlopen
from pykml.parser import parse
from json import dumps

def get_coordinates_from_kml(url):
    """ 
    Retira de um arquivo kml uma lista de coordenadas (longitudes e latitudes)
    @param url: a url do arquivo kml do google maps
    @return: uma lista com todas as longitudes e latitudes presentes no arquivo kml.
    """

    lng_lat_list = []
    try:
        kml_file = urlopen(url, data=None, timeout=30)
        root_tag = parse(kml_file).getroot()
        coordinates_text = root_tag.Document.Placemark.LineString.coordinates.text
        coordinates_list = coordinates_text.replace(' ','').replace('\n', ',').split(',')
        coordinates_list = coordinates_list[1:-1]

        # coordinates_list recebeu coordenadas do arquivo kml na sequencia: longitude, latitude, altitude,...
        # altitude = indices multiplos de 3
        lng_lat_list = [coordinate for coordinate in coordinates_list if (coordinates_list.index(coordinate) + 1) % 3 != 0]
    except Exception:
        pass

    return lng_lat_list


def coordinates_to_json(lng_lat_list):
    """ 
    Converte uma lista de coordenadas para o formato json
    @param lng_lat_list: uma lista de coordenadas
    @return: um arquivo json contendo as longitudes e latitudes de cada vertice da rota.
    """

    vertices = []
    route = {'Rota': vertices}

    if lng_lat_list:
        for coordinate in lng_lat_list:
            if lng_lat_list.index(coordinate) % 2 == 0:
                vertex = {}
                vertex['longitude'] = coordinate
            else:
                vertex['latitude'] = coordinate
                vertices.append(vertex)
        #route['Rota'] =  vertices
    return dumps(route)