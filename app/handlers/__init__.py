from .start_handlers import router as start_router
from .admin_handlers import router as admin_router
from .registration_handlers import router as registration_router
from .reregistration_handlers import router as reregistration_router

routers = [
    start_router,
    admin_router,
    registration_router,
    reregistration_router,
]
