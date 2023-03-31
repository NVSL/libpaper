#!/usr/bin/env python3
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


def call(cmd, *argc, **kwargs):
    print(f"Executing: {cmd}")
    return subprocess.check_call(cmd, *argc, shell=True, **kwargs)

def main(argv=None):

    load_args(argv)
    
    if not args.force:
        assert re.match("\d\d\d\d", args.year), "{} is not a correctly formatted year.".format(args.year)
        assert not re.search("\s|\.", args.topic), "topic can't have spaces."
        assert re.match("[A-Z]*", args.conference), "Conference should be all caps"
        
    name = "{}{}-{}".format(args.year, args.conference, args.topic)

    assert not call("ls")

    assert not call(f"""gh auth login --web"""), "Authentication failed"
    assert not call(f"""gh config set git_protocol ssh -h github.com"""), "Couldn't set gh protocol to ssh"
    assert not call(f"""gh repo create --private --template {args.template} -y NVSL/{name}"""), "Couldn't create repo"
   
    assert not call(f"""gh repo clone NVSL/{name}"""), "Couldn't create repo"
    assert not call("make; make test", cwd=name), "Test build failed"

if __name__ == "__main__":
    main()



