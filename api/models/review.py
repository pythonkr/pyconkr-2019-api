from django.contrib.auth import get_user_model
from django.db import models

from api.models.program import Presentation

UserModel = get_user_model()


class CFPReview(models.Model):
    owner = models.ForeignKey(UserModel, null=True, on_delete=models.SET_NULL)
    presentation = models.ForeignKey(Presentation, null=True,
                                     related_name='cfp_review_set',
                                     on_delete=models.SET_NULL)
    comment = models.TextField(blank=True, default='')
    submitted_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def submitted(self):
        return bool(self.submitted_at)
