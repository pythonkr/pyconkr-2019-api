MY_PRESENTATION_PROPOSAL= '''
query getMyPresentationProposal{
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
mutation createOrUpdatePresentationProposal($data: PresentationProposalInput!) {
    createOrUpdatePresentationProposal(data: $data) {
        proposal {
            name
            backgroundDesc
            category {
                id
                name
                nameKo
                nameEn
                slug
                visible
            }
            difficulty {
                id
                name
                nameKo
                nameEn
            }
            detailDesc
            language
            duration
            isPresentedBefore
            placePresentedBefore
            presentedSlideUrlBefore
            comment
            submitted
        }
        isAgreedAll
    }
}
'''
