#!/usr/bin/python3
# encoding: utf-8

import sys

from workflow import Workflow3, ICON_ERROR, ICON_INFO, ICON_WARNING

def main(wf):
    try:
        data = wf.args[0].split(" ")
        if len(data) != 2:
            return 1

        [key, value] = data
        wf.logger.debug('Saving %r', key)

        if key in ['user', 'org']:
            wf.store_data(key, value)
        elif key == 'token':
            wf.save_password('ghpr-api-key', token)
    except Exception as err:
        wf.logger.debug('err=%r', err)

if __name__ == '__main__':
    wf = Workflow3()
    sys.exit(wf.run(main))
