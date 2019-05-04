ASSIGN_CFP_REVIEW = '''
mutation AssignCfpReview($categoryIds: [ID]!, $languages: [LanguageNode]!) {
    assignCfpReview(categoryIds:$categoryIds, languages: $languages) {
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
