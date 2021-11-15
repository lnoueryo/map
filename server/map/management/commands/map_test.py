import unittest
from django.core.management.base import BaseCommand
import map.tests as tests
def execute():
    suite = unittest.TestLoader().loadTestsFromModule(tests, pattern=None)
    unittest.TextTestRunner().run(suite)

class Command(BaseCommand):

    def handle(self, *args, **options):
        execute()