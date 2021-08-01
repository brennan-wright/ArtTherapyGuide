# models.py
import factory
from django.db import models


class Country(models.Model):
    name = models.CharField()
    lang = models.CharField()


class Region(models.Model):
    name = models.CharField()
    lang = models.CharField()
    country = models.ForeignKey(Country)


class City(models.Model):
    name = models.CharField()
    city = models.ForeignKey(Region)
    country = models.ForeignKey(Country)


# factories.py
class CountryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Country

    name = factory.Iterator(["France", "Italy", "Spain"])
    lang = factory.Iterator(['fr', 'it', 'es'])


class RegionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Region

    name = "John"
    lang = factory.SelfAttribute('country.lang')
    country = factory.SubFactory(CountryFactory)


class CityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = City

    name = "ACME, Inc."
    country = factory.SubFactory(CountryFactory)
    region = factory.SubFactory(
        RegionFactory, country=factory.SelfAttribute('..country'))
