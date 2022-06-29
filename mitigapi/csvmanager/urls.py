from django.urls import path

from .views import AddView, ListView, HeadersView

urlpatterns = [
    path('add/', AddView.as_view()),
    path('list/<str:topic>/', ListView.as_view()),
    path('headers/<str:key>/', HeadersView.as_view()),
]
