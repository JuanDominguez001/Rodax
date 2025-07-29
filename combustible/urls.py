from rest_framework.routers import DefaultRouter
from .views import CombustibleViewSet

router = DefaultRouter()
router.register(r"combustibles", CombustibleViewSet, basename="combustible")

urlpatterns = router.urls

