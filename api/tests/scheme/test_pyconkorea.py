from django.utils.timezone import get_current_timezone
from api.tests.base import BaseTestCase
from api.schema import schema

TIMEZONE = get_current_timezone()


class PyconKoreaTest(BaseTestCase):
    def test_retrieve_conference(self):
        query = '''
        query {
            pyconKorea {
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
            
                babycareTicketStartAt
                babycareTicketFinishAt
            
                youngcoderTicketStartAt
                youngcoderTicketFinishAt
            }
        }
        '''

        result = schema.execute(query)
        response_pyconkorea = result.data['pyconKorea']
        self.assertIsNotNone(response_pyconkorea)
        self.assertEqual('파이콘 한국 2019', response_pyconkorea['nameKo'])
        self.assertEqual('PyCon Korea 2019', response_pyconkorea['nameEn'])
