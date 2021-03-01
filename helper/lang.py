#!/usr/bin/env python
# encoding: utf-8

from datetime import datetime

status = {
    'CHANGES_REQUESTED': 'Changes requested',
    'APPROVED': 'Approved',
    'REVIEW_REQUIRED': 'Review required'
}

status_icon = {
    'CHANGES_REQUESTED': 'icon-pr-blocked.png',
    'APPROVED': 'icon-pr-approved.png',
    'REVIEW_REQUIRED': 'icon-pr.png'
}

merge_status = {
    'MERGEABLE': 'Can be merged',
    'CONFLICTING': 'Need to fix conflicts',
    'UNKNOWN': 'Unknown'
}

my_review_status = {
    'PENDING': 'I was reviewing %s',
    'COMMENTED': 'I commented %s',
    'APPROVED': u'I approved %s ✅',
    'CHANGES_REQUESTED': u'I requested changes %s ❌',
    'DISMISSED': u'My review is dismissed %s ❕'
}

status_check_state = {
    'EXPECTED': u'❔ Check expected',
    'ERROR': u'❗️ Check error',
    'FAILURE': u'❌ Check failed',
    'PENDING': u'🔆 Check pending',
    'SUCCESS': u'✅ Check successful'
}

def prettytime(date_string):
    date = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
    diff = datetime.utcnow() - date
    s = diff.seconds
    if diff.days > 7 or diff.days < 0:
        return date.strftime('%d %b %y')
    elif diff.days == 1:
        return 'yesterday'
    elif diff.days > 1:
        return '{} days ago'.format(diff.days)
    elif s <= 1:
        return 'just now'
    elif s < 60:
        return '{} seconds ago'.format(s)
    elif s < 120:
        return '1 minute ago'
    elif s < 3600:
        return '{} minutes ago'.format(s/60)
    elif s < 7200:
        return '1 hour ago'
    else:
        return '{} hours ago'.format(s/3600)

def requested_review_status(user, reviewRequests):
    if user in reviewRequests:
        return u'‼️ I need to review. '
    return ''

def review_status(reviews):
    if len(reviews) == 0:
        return u'I have not reviewed yet❗️'

    my_review = reviews[0] # expect only one
    return my_review_status[my_review['state']] % prettytime(my_review['submittedAt'])

def get_display(user, pr):
    icon = 'icon-pr-draft.png' if pr['isDraft'] else status_icon[pr['reviewDecision']]
    title = '[%s] %s' % (pr['repository'], pr['title'])
    my_review = u'%s%s • %s • %s' % (
        requested_review_status(user, pr['reviewRequests']),
        review_status(pr['reviews']),
        status[pr['reviewDecision']],
        status_check_state[pr['statusCheck']]
    )
    assigned_to_me = 'Assigned to me.' if user in pr['assignees'] else ''
    info = 'Opened %s by %s. Updated %s. %s' % (prettytime(pr['createdAt']), pr['author'], prettytime(pr['updatedAt']), assigned_to_me)
    draft = '[DRAFT] ' if pr['isDraft'] else ''
    details = '%sChanged files: %d. %s' % (draft, pr['changedFiles'], merge_status[pr['mergeable']])

    return {
        'icon': ('icons/%s' % icon),
        'title': title,
        'info': info,
        'my_review': my_review,
        'details': details
    }
