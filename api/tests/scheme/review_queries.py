ASSIGN_CFP_REVIEWS = '''
mutation AssignCfpReviews($categoryIds: [ID]!, $languages: [LanguageNode]!) {
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
mutation SubmitCfpReviews($reviews: [ReviewNode]!) {
    submitCfpReview(reviews:$reviews) {
        success
    }
}
'''