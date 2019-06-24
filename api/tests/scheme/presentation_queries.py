PRESENTATIONS = '''
query getPresentations {
    presentations {
        id
        isKeynote
        name
        desc
        owner {
            username
        }
        backgroundDesc
        language
        duration
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
        recordable
        submitted
        accepted
    }
}
'''

PRESENTATION = '''
query getPresentation($id: Int!) {
    presentation(id: $id) {
        id
        isKeynote
        name
        desc
        owner {
            username
        }
        backgroundDesc
        language
        duration
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
        recordable
        submitted
        accepted
    }
}
'''

MY_PRESENTATION_PROPOSAL = '''
query getMyPresentationProposal {
    myPresentationProposal {
        name
        desc
        owner {
            username
        }
        backgroundDesc
        detailDesc
        language
        duration
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
        isPresentedBefore
        placePresentedBefore
        presentedSlideUrlBefore
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
            desc
            backgroundDesc
            detailDesc
            language
            duration
            isPresentedBefore
            placePresentedBefore
            presentedSlideUrlBefore
            submitted
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
        }
    }
}
'''
