from google.appengine.api import urlfetch
from xml.etree.ElementTree import *

from django.http import *

from jelenlet.models import *

COUNTRIES_FEED='http://api.erepublik.com/v1/feeds/countries'

def parse( url ) :
    result = urlfetch.fetch(url)
    if result.status_code == 200:
        return ElementTree(fromstring(result.content))

def save_countries(request):
    countries_tree = parse(COUNTRIES_FEED)
    countries = []
    for country in countries_tree.findall('country'):
        c = Country()
        c.initials = country.find('initials').text
        c.id = int(country.find('id').text)
        c.name = country.find('name').text
        c.continent = country.find('continent').text
        c.put()
        list_regions(c.id)
        countries.append({
            'id': country.find('id').text,
            'name': country.find('name').text,
        })

def save_regions(country_id):
    country_tree = parse(COUNTRIES_FEED + '/' + str(country_id))
    for region in country_tree.findall('regions/region'):
        r = Region()
        r.id = int(region.find('id').text)
        r.country_id = country_id
        r.name = region.find('name').text
        r.put()

def get_regions(request):
    regions = Region.all()
    regions = regions.fetch(regions.count())
    r_list = '{ '
    for region in regions:
        r_list += '"' + region.name + '" '
    r_list += '}'
    return HttpResponse(r_list, mimetype="text/plain")
