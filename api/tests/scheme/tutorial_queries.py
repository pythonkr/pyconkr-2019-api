TUTORIALS = '''
query getTutorials {
    tutorials {
        id
        name
        desc
        numOfParticipants
        language
        owner {
            username
        }
        difficulty {
            id
            name
            nameKo
            nameEn
        }
        place {
            name
        }
        startedAt
        finishedAt
        submitted
        accepted
    }
}
'''

TUTORIAL = '''
query getTutorial($id: Int!) {
    tutorial(id: $id) {
        id
        name
        desc
        numOfParticipants
        language
        owner {
            username
        }
        difficulty {
            id
            name
            nameKo
            nameEn
        }
        place {
            name
        }
        startedAt
        finishedAt
        submitted
        accepted
    }
}
'''