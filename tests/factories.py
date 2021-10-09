
import factory
from directive.models import (DirectiveDiagnosis, DirectiveInstruction,
                              DirectiveMaterial, DirectiveObjective,
                              DirectivePage, DirectivePopulation)
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


class DirectiveInstructionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = DirectiveInstruction
    instruction = factory.Faker('sentence')


class DirectiveMaterialFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = DirectiveMaterial
    material = factory.Faker('sentence')


class DirectiveObjectiveFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = DirectiveObjective
    objective = factory.Faker('sentence')


class DirectivePageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = DirectivePage
    uuid = factory.Faker('uuid4')
    title = factory.Faker('sentence')
    intro = factory.Faker('sentence')
    discussion = factory.Faker('sentence')
    instruction = factory.RelatedFactory(
        DirectiveInstructionFactory,
        factory_related_name='directive',
        instruction=factory.Faker('sentence'),
    )
    material = factory.RelatedFactory(
        DirectiveMaterialFactory,
        factory_related_name='directive',
        material=factory.Faker('sentence'),
    )
    objective = factory.RelatedFactory(
        DirectiveObjectiveFactory,
        factory_related_name='directive',
        objective=factory.Faker('sentence'),
    )

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
