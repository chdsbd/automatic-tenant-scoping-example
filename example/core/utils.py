from typing import Optional
import threading

from .models import Tenant


class State(threading.local):
    current_tenant = None


def get_current_tenant() -> Optional[Tenant]:
    """Retrieve current tenant from TLS"""
    return State.current_tenant
