#!/usr/bin/env python

from __future__ import print_function
import argparse
import subprocess
import re
import json
import sys


#TODO call in newpaper.py
#TODO use cookie between curl requests
#TODO domain name for buildbot

WEBHOOK_URL = 'http://52.53.183.89:9000/'
PERM_URLBASE = 'http://go.ucsd.edu/paper/'


def load_args(argv=None):
    parser = argparse.ArgumentParser(description="Add an existing paper to buildbot.")

    parser.add_argument("--repo", help="Repo name, e.g. 2019ArXiv-3DXPoint")
    parser.add_argument("--github-user", required=True, help="Your github username")

    global args
    if argv != None:
        args = parser.parse_args(args=argv)
    else:
        args = parser.parse_args()


def main(argv=None):

    load_args(argv)

    # Grant nvsl-bot read access
    # PUT /repos/:owner/:repo/collaborators/:username
    result = subprocess.check_output("""curl -c .autobuild.cookie -s -L -u {user} -X PUT https://api.github.com/repos/NVSL/{repo}/collaborators/nvsl-bot -d '{{"permission":"pull"}}' """.format(repo=args.repo, user=args.github_user), shell=True)

    if result != b'':
        print("Add nvsl-bot failed:\n{}".format(result))
        sys.exit(1)
    print("Bot user added.")

    # Add webhook
    # POST /repos/:owner/:repo/hooks
    payload ={}
    payload['name'] = 'web'
    payload['active'] = True
    payload['events'] = ['push']
    payload['config'] = { 'url': WEBHOOK_URL, 'content_type': 'json' }
    cmd = """curl -c .autobuild.cookie -s -L -u {user} -X POST https://api.github.com/repos/NVSL/{repo}/hooks -d '{data}' """.format(repo=args.repo, user=args.github_user, data=json.dumps(payload))
    result = subprocess.check_output(cmd, shell=True)
    r = json.loads(result)

    if "id" not in r:
        print("Add webhook failed:\n{}".format(result))
        sys.exit(1)
    print("Webook added.")


    print("--------Paper Permanent URL:--------")
    print(PERM_URLBASE+'{repo}.pdf\t\t(for paper.pdf)'.format(repo=args.repo))
    print(PERM_URLBASE+'{repo}/file.pdf\t(for other PDF files)'.format(repo=args.repo))


if __name__ == "__main__":
    main()



