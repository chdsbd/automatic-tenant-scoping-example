from django.test import TestCase

from .models import Project, Tenant
from .utils import State


class ProjectModelTests(TestCase):
    def setUp(self):
        tenant_a = Tenant.objects.create()
        tenant_b = Tenant.objects.create()
        Project.objects.create(name="alpha", description="desc", tenant=tenant_a)
        Project.objects.create(name="bravo", description="desc", tenant=tenant_a)
        Project.objects.create(name="charlie", description="desc", tenant=tenant_b)
        # configure thread local storage
        State.current_tenant = tenant_a

    def test_tenant_isolate(self):
        self.assertEqual(
            Project.objects.count(),
            2,
            "the current user should only see their projects",
        )
        self.assertEqual(
            Project.tenant_unconstrained_unsafe.count(),
            3,
            "unconstrained queries should return everything",
        )
