from rest_framework.routers import DefaultRouter
from .views import ServicioViewSet       

router = DefaultRouter()
router.register(r"mantenimientos", ServicioViewSet, basename="mantenimiento")

urlpatterns = router.urls
