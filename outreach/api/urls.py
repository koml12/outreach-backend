from rest_framework import routers
from api.views import PersonViewSet

router = routers.SimpleRouter()
router.register(r'people', PersonViewSet)
urlpatterns = router.urls