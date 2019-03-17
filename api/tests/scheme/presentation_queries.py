MY_PRESENTATION_PROPOSAL = '''
query {
    myPresentationProposal {
        name
        owner {
            username
        }
        backgroundDesc
        detailDesc
        language
        duration
        category {
            name
            nameKo
            nameEn
            slug
            visible
        }
        difficulty {
            name
            nameKo
            nameEn
        }
        isPresentedBefore
        placePresentedBefore
        presentedSlideUrlBefore
        comment
        isAgreed
        recordable
        submitted
        accepted
    }
}
'''

CREATE_OR_UPDATE_PRESENTATION_PROPOSAL = '''
mutation createOrUpdatePresentationProposal($input: PresentationProposalInput!) {
    createOrUpdatePresentationProposal(input: $input) {
        proposal {
          name
          backgroundDesc
          detailDesc
          language
          duration
          isPresentedBefore
          placePresentedBefore
          presentedSlideUrlBefore
          comment
          submitted
        }
        success
    }
}
'''
