from django.db import models


class Tenant(models.Model):
    """Simple model to restrict projects"""


class MissingTenantException(RuntimeError):
    """Tenant is required to access `.objects` of tenant restricted model"""


class TenantManager(models.Manager):
    """Manager that automatically filters Projects to the current tenant"""

    def get_queryset(self):
        """Filter to current tenant by default"""
        from .utils import get_current_tenant

        rv = get_current_tenant()
        if rv is None:
            raise MissingTenantException()
        return super().get_queryset().filter(tenant=rv)


class TenantModelMixin(models.Model):
    """
    Provide tenant-based automatic scoping of models

    example:
        Project.objects.all()
        # returns only projects for the current tenant
        Project.tenant_unconstrained_unsafe().all()
        # returns all projects
    """

    class Meta:
        abstract = True

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    # unconstrained manager must come first for it to be default
    tenant_unconstrained_unsafe = models.Manager()
    objects = TenantManager()


class Project(TenantModelMixin, models.Model):
    """Model associated with individual tenants"""

    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
