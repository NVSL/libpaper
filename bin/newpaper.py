#!/usr/bin/env python

from __future__ import print_function
import argparse
import subprocess
import re
import json
import sys

def load_args(argv=None):
    parser = argparse.ArgumentParser(description="Create a new paper")

    parser.add_argument("--topic", required=True, help="Short name for the paper. e.g. 'Nova' or 'MonetaNet'")
    parser.add_argument("--conference", required=True, help="Target venue. e.g., 'OSDI' or 'ASPLOS'")
    parser.add_argument("--year", required=True, help="Year of target publication. e.g. '2019'")
    parser.add_argument("--force", help="Don't validate paper name info")
    parser.add_argument("--github-user", required=True, help="Your github username")
    parser.add_argument("--template", default="git@github.com:NVSL/paper-template.git", help="Git repo to checkout for template file")

    global args
    if argv != None:
        args = parser.parse_args(args=argv)
    else:
        args = parser.parse_args()

def clone(name):
    assert not subprocess.check_call("git clone {git} {name}".format(name=name,git=args.template), shell=True), "Couldn't clone paper template"
    assert not subprocess.check_call("make setup", shell=True, cwd=name)
    

def main(argv=None):

    load_args(argv)

    if not args.force:
        assert re.match("\d\d\d\d", args.year), "{} is not a correctly formatted year.".format(args.year)
        assert not re.search("\s|\.", args.topic), "topic can't have spaces."
        assert re.match("[A-Z]*", args.conference), "Conference should be all caps"
    
    name = "{}{}-{}".format(args.year, args.conference, args.topic)

    clone(name)
        
    result = subprocess.check_output("""curl -u {user} https://api.github.com/orgs/NVSL/repos -d '{{"name":"{repo}", "private":true}}'""".format(user=args.github_user, repo="{}".format(name)), shell=True)
    r = json.loads(result)

    if "id" not in r:
        print("Creation Failed:\n{}".format(result))
        sys.exit(1)
    print("Created Repo!")


    assert not subprocess.check_call("git remote remove origin", shell=True, cwd=name), "Couldn't remove remote origin"
    assert not subprocess.check_call("git remote add origin {}".format(r['clone_url']), shell=True, cwd=name), "Couldn't remove remote origin"
    assert not subprocess.check_call("git push --set-upstream origin master", shell=True, cwd=name), "Couldn't set upstream branch"
    assert not subprocess.check_call("git push", shell=True, cwd=name), "Couldn't push"
    assert not subprocess.check_call("make test", shell=True, cwd=name), "Test build failed"

if __name__ == "__main__":
    main()



