#!/usr/bin/python3
# encoding: utf-8

import sys

from workflow import Workflow3, ICON_ERROR, ICON_INFO, ICON_WARNING

def extract_input(input):
    items = input.split(" ")
    if len(items) != 2:
        return None

    [key, value] = items
    if not value or key not in ['user', 'org', 'token']:
        return None
    else:
        return [key, value]


def main(wf):
    try:
        data = extract_input(wf.args[0])
        if not data:
            wf.add_item('Incorrect data', 'Type user, org or token followed by the value', valid=False, icon=ICON_WARNING)
            wf.send_feedback()
            return 1

        [key, value] = data
        wf.logger.debug('key=%r, value=%r', key, value)
        query = ('%s %s' % (key, value))
        wf.add_item('Set %s as %s' % (key, value), arg=query, valid=True, icon=ICON_INFO)
    except Exception as err:
        wf.logger.debug('err=%r', err)
        wf.add_item('Error', 'Bad data', valid=False, icon=ICON_ERROR)
    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow3()
    sys.exit(wf.run(main))
