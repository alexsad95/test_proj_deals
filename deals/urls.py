from django.urls import path
from .views import DealView

app_name = "deals"

urlpatterns = [
    path('deals/', DealView.as_view()),
]