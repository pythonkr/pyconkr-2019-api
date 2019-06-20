ME = '''
query getMe {
    me {
        username
        isStaff
        isSuperuser
        isAgreed
        profile { 
            id
            oauthType
            name
            nameKo
            nameEn
            bio
            bioKo
            bioEn
            email
            phone
            organization
            nationality
            image
            avatarUrl
            blogUrl
            githubUrl
            facebookUrl
            twitterUrl
            linkedInUrl
            instagramUrl
        }
    }
}
'''

UPDATE_PROFILE = '''
mutation UpdateProfile($data: ProfileInput!) {
    updateProfile(data: $data) {
        profile { 
            id
            oauthType
            name       
            nameKo
            nameEn
            bio
            bioKo
            bioEn
            email
            phone
            organization
            nationality
            image
            avatarUrl
            blogUrl
            githubUrl
            facebookUrl
            twitterUrl
            linkedInUrl
            instagramUrl
        }
    }
}
'''

UPDATE_AGREEMENT = '''
mutation UpdateAgreement($isPrivacyPolicy: Boolean, $isTermsOfService: Boolean) {
    updateAgreement(isPrivacyPolicy: $isPrivacyPolicy, isTermsOfService: $isTermsOfService) {
        isAgreedAll
        user {
            username
            isStaff
            isSuperuser
            isAgreed
            profile { 
                id
                oauthType
                name       
                nameKo
                nameEn
                bio
                bioKo
                bioEn
                email
                phone
                organization
                nationality
                image
                avatarUrl
            }
        }
    }
}
'''

PATRONS = '''
query getPatrons {
    patrons {
        id
        name
        nameKo
        nameEn
        bio
        bioKo
        bioEn
        organization
        image
        avatarUrl
    }
}
'''
