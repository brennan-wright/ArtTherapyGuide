
import factory
from directive.models import (DirectiveAudience, DirectiveDiagnosis,
                              DirectiveIdentifiedPatient, DirectivePage,
                              DirectivePopulation)
from django.contrib.auth import get_user_model


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    username = factory.Faker('user_name')
    email = factory.Faker('ascii_email')
    password = factory.Faker('password')


class DirectiveDiagnosisFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = DirectiveDiagnosis
    name = factory.Faker('city')


class DirectivePopulationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = DirectivePopulation
    name = factory.Faker('city')


class DirectiveIdentifiedPatientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = DirectiveIdentifiedPatient
    name = factory.Faker('city')


class DirectiveAudienceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = DirectiveAudience
    name = factory.Faker('city')


class DirectivePageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = DirectivePage
    uuid = factory.Faker('uuid4')
    title = factory.Faker('sentence')
    updated = factory.Faker('date_time')

    @factory.post_generation
    def population(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for population in extracted:
                self.population.add(population)

    @factory.post_generation
    def diagnosis(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for diagnosis in extracted:
                self.diagnosis.add(diagnosis)

    @factory.post_generation
    def identified_patient(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for identified_patient in extracted:
                self.identified_patient.add(identified_patient)

    @factory.post_generation
    def audience(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for audience in extracted:
                self.audience.add(audience)
