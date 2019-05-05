ASSIGN_CFP_REVIEWS = '''
mutation assignCfpReviews($categoryIds: [ID]!, $languages: [LanguageNode]!) {
    assignCfpReviews(categoryIds:$categoryIds, languages: $languages) {
        reviews{
          id
          presentation {
            name
            nameKo
            nameEn
            language
            backgroundDesc
            duration
            category {
              name
              nameKo
              nameEn
            }
            difficulty {
              name
              nameKo
              nameEn
            }
            detailDesc
          }
          comment
          createdAt
          updatedAt
          
        }
    }
}
'''

ASSIGNED_CFP_REVIEWS = '''
query getAssignedCfpReviews {
    isCfpReviewSubmitted
    assignedCfpReviews {
      id
      presentation {
        name
        nameKo
        nameEn
        language
        backgroundDesc
        duration
        category {
          name
          nameKo
          nameEn
        }
        difficulty {
          name
          nameKo
          nameEn
        }
        detailDesc
      }
      comment
      createdAt
      updatedAt
    }
}
'''

SUBMIT_CFP_REVIEWS = '''
mutation submitCfpReviews($reviews: [ReviewInput]!) {
    submitCfpReviews(reviews:$reviews) {
        success
    }
}
'''