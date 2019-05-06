SPONSOR_LEVELS = '''
query getSponsorLevels {
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
        currentRemainingNumber
    }
}
'''

UPLOAD_BUSINESS_REGISTRATION_FILE = '''
mutation UploadBusinessRegistrationFile($file: Upload!) {
    uploadBusinessRegistrationFile(file: $file) {
        success
        file
    }
}
'''

DELETE_BUSINESS_REGISTRATION_FILE = '''
mutation DeleteBusinessRegistrationFile($sponsorId: ID!) {
    deleteBusinessRegistrationFile(sponsorId: $sponsorId) {
        success
    }
}
'''

UPLOAD_LOGO_IMAGE = '''
mutation UploadLogoImage($file: Upload!) {
    uploadLogoImage(file: $file) {
        success
        image
    }
}
'''

UPLOAD_LOGO_VECTOR = '''
mutation UploadLogoVector($file: Upload!) {
    uploadLogoVector(file: $file) {
        success
        image
    }
}
'''

CREATE_OR_UPDATE_SPONSER = '''
mutation CreateOrUpdateSponsor($data: SponsorInput!) {
    createOrUpdateSponsor(data: $data) {
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
            managerEmail
            businessRegistrationNumber
            businessRegistrationFile
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
query getMySponsor {
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
        managerEmail
        businessRegistrationNumber
        businessRegistrationFile
        url
        logoImage
        logoVector
        paidAt
        submitted
        accepted
    }
}
'''

SPONSORS = '''
query getSponsors {
  sponsors {
    name
    nameKo
    nameEn
    level {
      id
      name
    }
    desc
    descKo
    descEn
    url
    logoImage
    logoVector
  }
}
'''
