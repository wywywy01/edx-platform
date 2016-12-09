"""
Views for building plugins.
"""

from abc import abstractmethod

from django.conf import settings
from django.shortcuts import render_to_response
from django.templatetags.static import static

from web_fragments.views import FragmentView


class EdxFragmentView(FragmentView):
    """
    The base class of all Open edX fragment views.
    """
    USES_PATTERN_LIBRARY = True

    @staticmethod
    def get_css_dependencies(group):
        """
        Returns list of CSS dependencies belonging to `group` in settings.PIPELINE_JS.

        Respects `PIPELINE_ENABLED` setting.
        """
        if settings.PIPELINE_ENABLED:
            return [settings.PIPELINE_CSS[group]['output_filename']]
        else:
            return settings.PIPELINE_CSS[group]['source_filenames']

    @staticmethod
    def get_js_dependencies(group):
        """
        Returns list of JS dependencies belonging to `group` in settings.PIPELINE_JS.

        Respects `PIPELINE_ENABLED` setting.
        """
        if settings.PIPELINE_ENABLED:
            return [settings.PIPELINE_JS[group]['output_filename']]
        else:
            return settings.PIPELINE_JS[group]['source_filenames']

    @abstractmethod
    def vendor_js_dependencies(self, request, *args, **kwargs):
        """
        Returns list of the vendor JS files that this view depends on.
        """
        return []

    @abstractmethod
    def js_dependencies(self, request, *args, **kwargs):
        """
        Returns list of the JavaScript files that this view depends on.
        """
        return []

    @abstractmethod
    def css_dependencies(self, request, *args, **kwargs):
        """
        Returns list of the CSS files that this view depends on.
        """
        return []

    def add_resource_urls(self, fragment):
        """
        Adds URLs for JS and CSS resources that this XBlock depends on to `fragment`.
        """
        # Head dependencies
        for vendor_js_file in self.vendor_js_dependencies():
            fragment.add_resource_url(static(vendor_js_file), "application/javascript", "head")

        for css_file in self.css_dependencies():
            fragment.add_css_url(static(css_file))

        # Body dependencies
        for js_file in self.js_dependencies():
            fragment.add_javascript_url(static(js_file))

    def render_standalone_html(self, fragment):
        """
        Renders a standalone version of this fragment.
        """
        context = {
            'settings': settings,
            'fragment': fragment,
            'uses-pattern-library': self.USES_PATTERN_LIBRARY,
        }
        return render_to_response(settings.STANDALONE_FRAGMENT_VIEW_TEMPLATE, context)
