
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
            name
            nameKo
            nameEn
            descKo
            descEn
            url
        }
    }
}
'''