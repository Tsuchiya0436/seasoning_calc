from django.contrib import admin
from django.urls import path
from .views import SeasoningCalculation, SeasoningMenu, SeasoningList

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', SeasoningMenu.as_view(), name="menu"),
    path('calculator/', SeasoningCalculation.as_view(), name="calculator"),
    path('list/', SeasoningList.as_view(), name="list"),
]
