"""Library (API) specific models."""

from http import HTTPStatus

from django.db import models

from core.mixins import Model


class CachedRequest(Model):
    """Cached request model."""

    path = models.CharField(max_length=255, null=False, blank=False)
    params = models.JSONField()
    data = models.JSONField()
    status_code = models.IntegerField(
        null=False,
        blank=False,
        default=HTTPStatus.IM_A_TEAPOT,
    )
    user = models.ForeignKey("api.AppUser", on_delete=models.PROTECT, null=True)

    objects = models.Manager()
