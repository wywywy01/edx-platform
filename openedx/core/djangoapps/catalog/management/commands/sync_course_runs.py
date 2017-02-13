"""
Sync course runs from catalog service.
"""
import logging

from django.core.management.base import BaseCommand
from opaque_keys.edx.keys import CourseKey

from catalog.utils import get_catalog_course_runs
from content.course_overviews.models import CourseOverview

logger = logging.getLogger(__name__)


def fetch_catalog_course_runs():
    """
    Fetch catalog course runs from catalog service for all course overview records.
    """
    course_overviews = CourseOverview.objects.all()
    return get_catalog_course_runs(
        course_keys=course_overviews.values_list('id', flat=True)
    )


def update_course_overviews(course_runs):
    """
    Refresh marketing urls for the given catalog course runs.

    Arguments:
        course_runs: A list containing catalog course runs.
    """
    for course_run in course_runs:
        marketing_url = course_run.get('marketing_url')
        course_key = CourseKey.from_string(course_run.get('key'))
        try:
            course_overview = CourseOverview.objects.get(id=course_key)
        except CourseOverview.DoesNotExist:
            # That's a case when a course gets deleted from CourseOverview
            # after the command has been run for it.
            continue

        # Check whether course overview's marketing url is outdated - this would save a db hit.
        if course_overview.marketing_url != marketing_url:
            course_overview.marketing_url = marketing_url
            course_overview.save()


class Command(BaseCommand):
    """
    Sync marketing urls from catalog service to CourseOverview.
    """
    help = 'Refresh marketing urls from catalog service.'

    def handle(self, *args, **options):
        update_course_overviews(course_runs=fetch_catalog_course_runs())
