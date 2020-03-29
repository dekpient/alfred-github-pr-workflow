#!/usr/bin/python3
# encoding: utf-8

import sys
from workflow import Workflow3, PasswordNotFound, ICON_WARNING

from helper.query import get_org_prs
from helper.lang import get_display

def search_key_for_pr(pr):
    elements = []
    elements.append(pr['title'])
    elements.append(pr['author'])
    elements.append(pr['repository'])
    elements.append(pr['reviewDecision'])
    return u' '.join(elements)

def main(wf):
    try:
        auth_token = wf.get_password('ghpr-api-key')
    except PasswordNotFound:
        wf.add_item('No API token set',
                    'Please use ghpr-config to set your GitHub personal token.',
                    arg='https://github.com/settings/tokens/new',
                    valid=True,
                    icon=ICON_WARNING)
        wf.send_feedback()
        return 1

    org = wf.stored_data('org')
    user = wf.stored_data('user')

    if not org or not user:
        wf.add_item('User and org name not configured',
                    'Please use ghpr-config to set your details.',
                    valid=False,
                    icon=ICON_WARNING)
        wf.send_feedback()
        return 1

    query = wf.args[0] if len(wf.args) else None
    prs = wf.cached_data('org_prs', get_org_prs(user, org, auth_token), max_age=60)

    if query:
        prs = wf.filter(query, prs, key=search_key_for_pr)

    for pr in prs:
        display = get_display(user, pr)
        it = wf.add_item(title=display['title'], subtitle=display['my_review'], arg=pr['url'], valid=True, icon=display['icon'])
        m = it.add_modifier('cmd', subtitle=display['info'], arg='%s/files' % pr['url'])
        mm = it.add_modifier('alt', subtitle=display['details'], arg='%s#partial-pull-merging' % pr['url'])

    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow3()
    sys.exit(wf.run(main))
