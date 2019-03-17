ME = '''
query {
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
        }
    }
}
'''

UPDATE_PROFILE = '''
    mutation UpdateProfile($profileInput: ProfileInput!) {
        updateProfile(profileInput: $profileInput) {
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
