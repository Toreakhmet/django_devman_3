from django.urls import reverse
from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from places.models import Place

JSON_DUMPS_PARAMS = {
    'indent': 2,
    'ensure_ascii': False
}


def get_place(request, place_id):
    place = get_object_or_404(Place, id=place_id)

    context = {
        "title": place.title,
        "imgs": [],
        "description_short": place.description_short,
        "description_long": place.description_long,
        "coordinates": {
            "lng": place.longitude,
            "lat": place.latitude
        }
    }
    for image in place.images.all().order_by('position'):
        context["imgs"].append(image.img.url)

    return JsonResponse(
        context,
        json_dumps_params=JSON_DUMPS_PARAMS
    )


def home_view(request):
    places = Place.objects.all()
    features = []
    for place in places:
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [place.longitude, place.latitude]
            },
            "properties": {
                "title": place.title,
                "placeId": place.id,
                "detailsUrl": reverse('place_details', kwargs={'place_id': place.id})
            }
        })
    places_geojson = {
        "type": "FeatureCollection",
        "features": features,
    }

    context = {
        "places_geojson": places_geojson,
    }
    return render(request, 'index.html', context)
