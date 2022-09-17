#!/usr/bin/python3
# encoding: utf-8

import json

from urllib import request

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
    pr['assignees'] = list(map(lambda n: n['login'], pr['assignees']['nodes']))

    try:
      pr['reviewRequests'] = list(map(lambda n: n['requestedReviewer']['login'], pr['reviewRequests']['nodes']))
    except Exception:
      pr['reviewRequests'] = list()

    pr['reviews'] = list(map(lambda n: {
        'reviewer': n['author']['login'],
        'state': n['state'],
        'submittedAt': n['submittedAt']
    }, pr['reviews']['nodes']))
    try:
      pr['statusCheck'] = pr['commits']['nodes'][0]['commit']['statusCheckRollup']['state']
    except Exception:
      pr['statusCheck'] = 'ERROR'
    return pr


def get_org_prs(user, org, auth_token):
    def get():
        search_url = 'https://api.github.com/graphql'
        data = query(org, user).encode()
        req =  request.Request(search_url, data=data, headers=headers(auth_token))
        response = request.urlopen(req).read().decode('utf-8')
        response_json = json.loads(response)
        nodes = response_json['data']['search']['nodes']
        return list(map(transform, nodes))

    return get
