
SPONSOR_LEVELS = '''
query {
    sponsorLevels {
        id
        name
        nameKo
        nameEn
        visible
        price
        limit
        ticketCount
        presentationCount
        boothInfo
        programGuide
        canProvideGoods
        openLunch
        logoLocations
        canRecruit
    }
}
'''

UPLOAD_BUSINESS_REGISTRATION_FILE = '''
mutation UploadBusinessRegistrationFile($file: Upload!) {
    uploadBusinessRegistrationFile(file: $file) {
        success
    }
}
'''

CREATE_OR_UPDATE_SPONSER = '''
mutation CreateOrUpdateSponsor($sponsorInput: SponsorInput!) {
    createOrUpdateSponsor(sponsorInput: $sponsorInput) {
        sponsor {
            id
            creator {
              profile {
                name
                nameKo
                nameEn
                email
              }
            }
            name
            nameKo
            nameEn
            level {
                id
                name
                price
                limit
                ticketCount
                presentationCount
                boothInfo
                programGuide
                canProvideGoods
                logoLocations
                canRecruit
            }
            desc
            descKo
            descEn
            managerName
            managerPhone
            managerSecondaryPhone
            managerEmail
            businessRegistrationNumber
            businessRegistrationFile
            contractProcessRequired
            url
            logoImage
            logoVector
            paidAt
            submitted
            accepted
        }
    }
}
'''

SUBMIT_SPONSOR = '''
mutation SubmitSponsor($submitted: Boolean!) {
    submitSponsor(submitted: $submitted) {
        success
    		submitted
    }
}
'''

MY_SPONSOR = '''
query {
    mySponsor {
        id
        creator {
          profile {
            name
            nameKo
            nameEn
            email
          }
        }
        name
        nameKo
        nameEn
        level {
            id
            name
            price
            limit
            ticketCount
            presentationCount
            boothInfo
            programGuide
            canProvideGoods
            logoLocations
            canRecruit
        }
        desc
        descKo
        descEn
        managerName
        managerPhone
        managerSecondaryPhone
        managerEmail
        businessRegistrationNumber
        businessRegistrationFile
        contractProcessRequired
        url
        logoImage
        logoVector
        paidAt
        submitted
        accepted
    }
}
'''