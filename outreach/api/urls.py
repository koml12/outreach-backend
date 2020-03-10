from rest_framework import routers
from api.views import RegistrationViewSet, EvaluatorViewSet, CandidateViewSet, EventViewSet, GetAuthToken
from django.urls import path

router = routers.SimpleRouter()

urlpatterns = [
    path("login/", GetAuthToken.as_view())
]

router.register("candidates", CandidateViewSet)
router.register("evaluators", EvaluatorViewSet)
router.register("registration", RegistrationViewSet)
router.register("event", EventViewSet)


urlpatterns = urlpatterns + router.urls