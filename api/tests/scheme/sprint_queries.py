SPRINTS = '''
query getSprints {
    sprints {
        id
        name
        desc
        programmingLanguage
        language
        opensourceDesc
        opensourceUrl
        owner {
            username
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

SPRINT = '''
query getSprint($id: Int!) {
    sprint(id: $id) {
        id
        name
        desc
        programmingLanguage
        language
        opensourceDesc
        opensourceUrl
        owner {
            username
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