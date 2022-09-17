#!/usr/bin/python3
# encoding: utf-8

import sys

from workflow import Workflow3, Variables, ICON_ERROR, ICON_INFO, ICON_WARNING

def main(wf):
    try:
        data = wf.args[0].split(" ")
        if len(data) != 2:
            return 1

        [key, value] = data
        wf.logger.debug('Saving %r', key)

        if key in ['user', 'org']:
            wf.store_data(key, value)
            print("Set your {0} to {1}".format(key, value))
        elif key == 'token':
            wf.save_password('ghpr-api-key', value)
            print("Saved your API token in Keychain")
        else:
            return 1
    except Exception as err:
        # wf.logger.exception(err)
        wf.logger.debug('err=%r', err)
        return 1

if __name__ == '__main__':
    wf = Workflow3()
    sys.exit(wf.run(main))
