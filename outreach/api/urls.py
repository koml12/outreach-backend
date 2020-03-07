from rest_framework import routers
from api.views import EvaluatorViewSet, SignupIntoEvent, CandidateViewSet, GetAuthToken
from django.urls import path

router = routers.SimpleRouter()

urlpatterns = [
    path("register/<int:event>/", SignupIntoEvent.as_view(), name="EvalRegister"),
    path("login/", GetAuthToken.as_view())
]

router.register("candidates",CandidateViewSet)
router.register("evaluators",EvaluatorViewSet)

urlpatterns = urlpatterns + router.urls