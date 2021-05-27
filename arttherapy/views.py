from django.db import DEFAULT_DB_ALIAS, connections
from django.db.migrations.executor import MigrationExecutor
from django.http import HttpResponse
from django.views.generic.base import View


class health_check(View):
    def get(self, request, *args, **kwargs):
        executor = MigrationExecutor(connections[DEFAULT_DB_ALIAS])
        plan = executor.migration_plan(executor.loader.graph.leaf_nodes())
        status = 503 if plan else 200
        return HttpResponse(status=status)