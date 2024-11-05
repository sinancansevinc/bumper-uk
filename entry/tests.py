from django.urls import reverse
from django.core.cache import cache
from rest_framework import status
from rest_framework.test import APITestCase
from entry.models import User, GuestEntry

class GuestEntryListCreateViewTests(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(name="test_user")
        self.entry_data = {
            "subject": "Test Subject",
            "message": "This is a test message.",
            "name": "test_user"
        }
        self.create_url = reverse('guest-entry-list-create')
        cache.clear()
    
    def test_create_guest_entry(self):
        response = self.client.post(self.create_url, self.entry_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(GuestEntry.objects.count(), 1)

        # After creation, cache should be cleared
        cached_data = cache.get("guest_entries")
        self.assertIsNone(cached_data)

    def test_get_guest_entries(self):
        # Create sample entries
        GuestEntry.objects.create(user=self.user, subject="Entry 1", message="Message 1")
        GuestEntry.objects.create(user=self.user, subject="Entry 2", message="Message 2")

        # First GET request caches the data
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("entries", response.data)
        self.assertEqual(len(response.data["entries"]), 2)  # Verify entry count

        # Verify data is cached
        cache_key = f"guest_entries"
        cached_data = cache.get(cache_key)
        self.assertIsNotNone(cached_data)
        self.assertIn("entries", cached_data)
        self.assertEqual(len(cached_data["entries"]), 2)

        # Invalidate cache by creating a new entry
        new_entry_data = {
            "subject": "New Subject",
            "message": "New message.",
            "name": "test_user"
        }
        self.client.post(self.create_url, new_entry_data, format='json')

        # Cache should be cleared after new entry creation
        self.assertIsNone(cache.get(cache_key))


class UserGuestEntryListViewTests(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(name="test_user")
        self.entry_1 = GuestEntry.objects.create(user=self.user, subject="Entry 1", message="Message 1")
        self.entry_2 = GuestEntry.objects.create(user=self.user, subject="Entry 2", message="Message 2")
        self.url = reverse('user-guest-entry-list')
        cache.clear()
    
    def test_get_users_with_entries(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("users", response.data)

        # Check user data in response
        users_data = response.data["users"]
        self.assertEqual(len(users_data), 1)
        self.assertEqual(users_data[0]["username"], "test_user")
        self.assertEqual(users_data[0]["total_messages"], 2)
        self.assertEqual(users_data[0]["last_entry"], f"{self.entry_2.subject} | {self.entry_2.message}")

        # Check that data is cached
        cached_data = cache.get("guest_users")
        self.assertIsNotNone(cached_data)

    def test_cache_invalidation_on_guest_entry_change(self):
        # Initial request to populate cache
        self.client.get(self.url)
        self.assertIsNotNone(cache.get("guest_users"))

        # Invalidate cache with a new entry creation
        new_entry_data = {
            "subject": "New Subject",
            "message": "New message.",
            "name": "test_user"
        }
        create_url = reverse('guest-entry-list-create')
        self.client.post(create_url, new_entry_data, format='json')

        # Verify cache is cleared after creation
        self.assertIsNone(cache.get("guest_users"))

        # Populate cache again, then delete an entry and verify invalidation
        self.client.get(self.url)
        self.assertIsNotNone(cache.get("guest_users"))

        # Delete an entry and ensure cache is cleared
        self.entry_1.delete()
        self.assertIsNone(cache.get("guest_users"))