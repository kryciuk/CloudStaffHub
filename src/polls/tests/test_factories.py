from django.test import TestCase

from polls.factories import PollFactory
from polls.models import Poll


class TestPollsFactories(TestCase):
    def test_poll_via_factory(self):
        PollFactory.create()
        self.assertEqual(Poll.objects.count(), 1)

    def test_poll_batch_factory(self):
        PollFactory.create_batch(5)
        self.assertEqual(Poll.objects.count(), 5)
