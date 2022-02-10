#!/usr/bin/python3
# encoding: utf-8

import json

from workflow import web


def query(org, username):
    # review:none
    # review:required
    # review:approved
    # review-requested:@me
    # review:changes-requested
    # -reviewed-by:@me
    q = """
{
  search(query: "org:%s is:pr is:open -author:app/dependabot", type: ISSUE, last: 100) {
    nodes {
      ... on PullRequest {
        author {
          login
        }
        assignees(last: 10) {
          nodes {
            login
          }
        }
        changedFiles
        url
        title
        isDraft
        mergeable
        reviewDecision
        reviewRequests(last: 10) {
          nodes {
            requestedReviewer {
              ... on User {
                login
              }
            }
          }
        }
        reviews(last: 1, author:"%s") {
          nodes {
            author {
              login
            }
            state
            submittedAt
          }
        }
        createdAt
        updatedAt
        repository {
          name
        }
        commits(last: 1) {
          nodes {
            commit {
              statusCheckRollup {
                state
              }
            }
          }
        }
      }
    }
  }
}
""" % (org, username)
    return json.dumps({ 'query': q })

def headers(auth_token):
    return {
        'content-type': 'application/json',
        'authorization': 'bearer %s' % auth_token
    }

# Unnest attributes
def transform(pr):
    pr['author'] = pr['author']['login']
    pr['repository'] = pr['repository']['name']
    pr['assignees'] = map(lambda n: n['login'], pr['assignees']['nodes'])

    try:
      pr['reviewRequests'] = map(lambda n: n['requestedReviewer']['login'], pr['reviewRequests']['nodes'])
    except Exception:
      pr['reviewRequests'] = []

    pr['reviews'] = map(lambda n: {
        'reviewer': n['author']['login'],
        'state': n['state'],
        'submittedAt': n['submittedAt']
    }, pr['reviews']['nodes'])
    try:
      pr['statusCheck'] = pr['commits']['nodes'][0]['commit']['statusCheckRollup']['state']
    except Exception:
      print pr['commits']['nodes']
      pr['statusCheck'] = 'ERROR'
    return pr


def get_org_prs(user, org, auth_token):
    def get():
        search_url = 'https://api.github.com/graphql'
        data = query(org, user)
        response = web.post(search_url, None, data, headers(auth_token))
        response.raise_for_status()
        nodes = response.json()['data']['search']['nodes']
        return map(transform, nodes)

    return get
