from django.urls import path
from rest_framework.routers import DefaultRouter

from entry.views import GuestEntryListCreateView, UserGuestEntryListView


router = DefaultRouter()
urlpatterns = [
    path('guest-entries/', GuestEntryListCreateView.as_view(), name='guest-entry-list-create'),
    path('users/',UserGuestEntryListView.as_view(), name='user-guest-entry-list')
]