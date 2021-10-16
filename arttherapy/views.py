from django.db import DEFAULT_DB_ALIAS, connections
from django.db.migrations.executor import MigrationExecutor
from django.http import HttpResponse
from django.views.generic.base import TemplateView, View


class health_check(View):
    def get(self, request, *args, **kwargs):
        executor = MigrationExecutor(connections[DEFAULT_DB_ALIAS])
        plan = executor.migration_plan(executor.loader.graph.leaf_nodes())
        if plan:
            status = 503
            data = "No Good"
        else:
            status = 200
            data = "All Good"
        return HttpResponse(data, status=status,)


class HomeView(TemplateView):
    '''
    Homepage view
    '''
    template_name = 'arttherapy/homepage.html'


class AboutView(TemplateView):
    '''
    About page view
    '''
    template_name = 'arttherapy/aboutpage.html'
