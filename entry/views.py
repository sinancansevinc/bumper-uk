from django.shortcuts import render
from entry.models import GuestEntry, User
from entry.pagination import StandardResultsSetPagination
from entry.serializers import GuestEntryCreateSerializer,GuestEntryReadSerializer, UserEntryReadSerializer
from rest_framework import generics
from rest_framework.response import Response
from django.db.models import Count, Max
from django.core.cache import cache

class GuestEntryListCreateView(generics.ListCreateAPIView):
    queryset = GuestEntry.objects.select_related('user').all().order_by('-created_at')
    serializer_class = GuestEntryCreateSerializer
    pagination_class = StandardResultsSetPagination

    # Get serializer for request type
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GuestEntryReadSerializer
        return GuestEntryCreateSerializer
    
    def list(self, request, *args, **kwargs):
        # Use a unique cache key for this view’s data
        cache_key = "guest_entries"
        cached_data = cache.get(cache_key)

        if cached_data:
            # Return cached data if available
            return Response(cached_data)

        # If no cached data, get and cache it
        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=300)
        return response

    def create(self, request, *args, **kwargs):
        # Remove cache after creating a new entry
        cache.delete("guest_entries")
        return super().create(request, *args, **kwargs)
    
class UserGuestEntryListView(generics.ListAPIView):
    queryset = User.objects.annotate(
        total_messages=Count('guest_user'),
        last_entry=Max('guest_user__created_at')
    ).prefetch_related('guest_user')
    serializer_class = UserEntryReadSerializer

    # Use the default list method and add new "users" key
    def list(self, request, *args, **kwargs):
        cache_key = "guest_users"
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response({"users":cached_data})

        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=300)
        return Response({"users":response.data})

    