from django.db import models


class Schedule(models.Model):
    name = models.CharField(max_length=50)

    conference_start_at = models.DateField(null=True, blank=True)
    conference_finish_at = models.DateField(null=True, blank=True)
    tutorial_start_at = models.DateField(null=True, blank=True)
    tutorial_finish_at = models.DateField(null=True, blank=True)
    sprint_start_at = models.DateField(null=True, blank=True)
    sprint_finish_at = models.DateField(null=True, blank=True)

    keynote_recommendation_start_at = models.DateTimeField(null=True, blank=True)
    keynote_recommendation_finish_at = models.DateTimeField(null=True, blank=True)
    keynote_recommendation_announce_at = models.DateTimeField(null=True, blank=True)

    presentation_proposal_start_at = models.DateTimeField(null=True, blank=True)
    presentation_proposal_finish_at = models.DateTimeField(null=True, blank=True)
    presentation_review_start_at = models.DateTimeField(null=True, blank=True)
    presentation_review_finish_at = models.DateTimeField(null=True, blank=True)
    presentation_announce_at = models.DateTimeField(null=True, blank=True)

    tutorial_proposal_start_at = models.DateTimeField(null=True, blank=True)
    tutorial_proposal_finish_at = models.DateTimeField(null=True, blank=True)
    tutorial_proposal_announce_at = models.DateTimeField(null=True, blank=True)
    tutorial_ticket_start_at = models.DateTimeField(null=True, blank=True)
    tutorial_ticket_finish_at = models.DateTimeField(null=True, blank=True)

    sprint_proposal_start_at = models.DateTimeField(null=True, blank=True)
    sprint_proposal_finish_at = models.DateTimeField(null=True, blank=True)
    sprint_proposal_announce_at = models.DateTimeField(null=True, blank=True)
    sprint_ticket_start_at = models.DateTimeField(null=True, blank=True)
    sprint_ticket_finish_at = models.DateTimeField(null=True, blank=True)

    sponsor_proposal_start_at = models.DateTimeField(null=True, blank=True)
    sponsor_proposal_finish_at = models.DateTimeField(null=True, blank=True)

    volunteer_recruiting_start_at = models.DateTimeField(null=True, blank=True)
    volunteer_recruiting_finish_at = models.DateTimeField(null=True, blank=True)
    volunteer_announce_at = models.DateTimeField(null=True, blank=True)

    lightning_talk_proposal_start_at = models.DateTimeField(null=True, blank=True)
    lightning_talk_proposal_finish_at = models.DateTimeField(null=True, blank=True)
    lightning_talk_announce_at = models.DateTimeField(null=True, blank=True)

    earlybird_ticket_start_at = models.DateTimeField(null=True, blank=True)
    earlybird_ticket_finish_at = models.DateTimeField(null=True, blank=True)

    financial_aid_start_at = models.DateTimeField(null=True, blank=True)
    financial_aid_finish_at = models.DateTimeField(null=True, blank=True)
    financial_aid_announce_at = models.DateTimeField(null=True, blank=True)

    patron_ticket_start_at = models.DateTimeField(null=True, blank=True)
    patron_ticket_finish_at = models.DateTimeField(null=True, blank=True)

    conference_ticket_start_at = models.DateTimeField(null=True, blank=True)
    conference_ticket_finish_at = models.DateTimeField(null=True, blank=True)

    babycare_ticket_start_at = models.DateTimeField(null=True, blank=True)
    babycare_ticket_finish_at = models.DateTimeField(null=True, blank=True)

    youngcoder_ticket_start_at = models.DateTimeField(null=True, blank=True)
    youngcoder_ticket_finish_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name
