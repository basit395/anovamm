import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','testproject.settings')


import django
django.setup()

from fin.models import textstream
from faker import Faker

fakegen = Faker()

def populate(N=5):
    for entry in range(N):

        fake_mytext= fakegen.sentence()
        fake_location = fakegen.country()

        textnew = textstream.objects.get_or_create(mytext=fake_mytext,location=fake_location)[0]

if __name__ == '__main__':
    print("aaaa")
    populate(2000)
    print("complete")
