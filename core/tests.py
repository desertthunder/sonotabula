import unittest

from django.test import TestCase


class CoreViewsTestCase(TestCase):
    """Core views test case."""

    @unittest.skip("TODO")
    def test_user_profile_view(self) -> None:
        """Test user profile view."""
        pass

    @unittest.skip("TODO")
    def test_user_saved_items_view(self) -> None:
        """Test user saved items view."""
        pass


class AppUserManagerTestCase(TestCase):
    """AppUserManager test case."""

    @unittest.skip("TODO")
    def test_from_spotify(self) -> None:
        """Test from_spotify method."""
        pass


class AppUserTestCase(TestCase):
    """AppUser model tests."""

    @unittest.skip("TODO")
    def test_str(self) -> None:
        """Test __str__ method."""
        pass

    @unittest.skip("TODO")
    def test_should_update(self) -> None:
        """Test should_update method."""
        pass

    @unittest.skip("TODO")
    def test_update_token_set(self) -> None:
        """Test update_token_set method."""
        pass

    @unittest.skip("Not implemented")
    def test_should_refresh_token(self) -> None:
        """Test should_refresh_token method."""
        pass
