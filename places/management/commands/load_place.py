from pathlib import Path
from urllib.parse import unquote

import requests
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.core.exceptions import MultipleObjectsReturned

from places.models import Place, Image


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('urls', nargs='+', type=str)

    def handle(self, *args, **options):
        for url in options['urls']:
            response = requests.get(url)
            response.raise_for_status()
            payload = response.json()
            try:
                place, created = Place.objects.get_or_create(
                    title=payload['title'],
                    defaults={
                        'description_short': payload['description_short'],
                        'description_long': payload['description_long'],
                        'latitude': payload['coordinates']['lat'],
                        'longitude': payload['coordinates']['lng']
                    }
                )
            except MultipleObjectsReturned:
                self.stderr.write(self.style.ERROR(
                    f'Multiple places found with title "{payload["title"]}"'))
                continue

            for index,img_url in enumerate(payload['imgs']):
                img_response = requests.get(img_url)
                img_response.raise_for_status()
                file_name = Path(unquote(img_url)).name
                Image.objects.create(
                    place=place,
                    img=ContentFile(img_response.content, name=file_name),
                    position=index
                )

            self.stdout.write(self.style.SUCCESS(
                f'Successfully loaded url "{url}"'))
