import itertools
from datetime import date

from django.test import TestCase

from recruitment.choices import (JOB_OFFER_CITIES_CHOICES,
                                 JOB_OFFER_LEVEL_CHOICES,
                                 POSITION_DEPARTMENT_CHOICES)
from recruitment.factories import JobOfferFactory, PositionFactory
from recruitment.models import JobOffer, Position


class TestPosition(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_objects = PositionFactory.create_batch(10)

    def test_position_objects_created_correctly(self):
        self.assertIsInstance(self.test_objects[0], Position)
        self.assertIsInstance(self.test_objects[5], Position)

    def test_if_position_level_assigned_correctly(self):
        self.assertIn(
            self.test_objects[4].level, itertools.chain(*JOB_OFFER_LEVEL_CHOICES)
        )
        self.assertIn(
            self.test_objects[7].level, itertools.chain(*JOB_OFFER_LEVEL_CHOICES)
        )

    def test_if_departament_assigned_correctly(self):
        self.assertIn(
            self.test_objects[2].departament,
            itertools.chain(*POSITION_DEPARTMENT_CHOICES),
        )
        self.assertIn(
            self.test_objects[8].departament,
            itertools.chain(*POSITION_DEPARTMENT_CHOICES),
        )


class TestJobOffer(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_objects = JobOfferFactory.create_batch(10)

    def test_job_offer_objects_created_correctly(self):
        self.assertIsInstance(self.test_objects[1], JobOffer)
        self.assertIsInstance(self.test_objects[6], JobOffer)

    def test_job_offer_attributes_assigned_correctly(self):
        test_object = self.test_objects[4]
        self.assertIsInstance(test_object.position, Position)
        self.assertIs(test_object.status, True or False)
        self.assertIn(test_object.city, itertools.chain(*JOB_OFFER_CITIES_CHOICES))
