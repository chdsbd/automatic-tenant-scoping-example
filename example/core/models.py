from django.db import models
from logging import getLogger

log = getLogger(__name__)


class Tenant(models.Model):
    """Simple model to restrict projects"""


class ProjectManager(models.Manager):
    """Manager that automatically filters Projects to the current tenant"""

    def get_queryset(self):
        """Filter to current tenant by default"""
        from .utils import get_current_tenant

        rv = get_current_tenant()
        if rv is None:
            log.info("missing current tenant")
            return super().get_queryset()
        return super().get_queryset().filter(tenant=rv)


class Project(models.Model):
    """Model associated with individual tenants"""

    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    objects = ProjectManager()
    tenant_unconstrained_unsafe = models.Manager()
