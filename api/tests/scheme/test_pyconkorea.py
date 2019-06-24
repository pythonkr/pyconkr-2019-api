from django.utils.timezone import get_current_timezone
from api.tests.base import BaseTestCase
from api.schema import schema

TIMEZONE = get_current_timezone()


class ScheduleTest(BaseTestCase):
    def test_retrieve_schedule(self):
        query = '''
        query {
            schedule {
                name
                nameKo
                nameEn
                conferenceStartAt
                conferenceFinishAt
                tutorialStartAt
                tutorialFinishAt
                sprintStartAt
                sprintFinishAt
            
                keynoteRecommendationStartAt
                keynoteRecommendationFinishAt
                keynoteRecommendationAnnounceAt
            
                presentationProposalStartAt
                presentationProposalFinishAt
                presentationReviewStartAt
                presentationReviewFinishAt
                presentationAnnounceAt
            
                tutorialProposalStartAt
                tutorialProposalFinishAt
                tutorialProposalAnnounceAt
                tutorialTicketStartAt
                tutorialTicketFinishAt
            
                sprintProposalStartAt
                sprintProposalFinishAt
                sprintProposalAnnounceAt
                sprintTicketStartAt
                sprintTicketFinishAt
            
                sponsorProposalStartAt
                sponsorProposalFinishAt
            
                volunteerRecruitingStartAt
                volunteerRecruitingFinishAt
                volunteerAnnounceAt
            
                lightningTalkProposalStartAt
                lightningTalkProposalFinishAt
                lightningTalkAnnounceAt
            
                earlybirdTicketStartAt
                earlybirdTicketFinishAt
            
                financialAidStartAt
                financialAidFinishAt
                financialAidAnnounceAt
            
                patronTicketStartAt
                patronTicketFinishAt
            
                conferenceTicketStartAt
                conferenceTicketFinishAt
            
                childcareTicketStartAt
                childcareTicketFinishAt
            
                youngcoderTicketStartAt
                youngcoderTicketFinishAt
            }
        }
        '''

        result = schema.execute(query)
        response_schedule = result.data['schedule']
        self.assertIsNotNone(response_schedule)
        self.assertEqual('파이콘 한국 2019', response_schedule['nameKo'])
        self.assertEqual('PyCon Korea 2019', response_schedule['nameEn'])
