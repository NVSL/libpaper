#!/usr/bin/env python3

import argparse
import sys
import re
import logging as log

def search_for_includes(files):
    r = []
    log.debug(f"Searching files: {files}")
    for t in files:
        r.append(t)
        log.debug(f"Adding {t} to results")
        with open(t, "r") as f:
            for l in f.readlines():
                l = re.sub("%.*", "", l)
                l = l.strip();
                m = re.search("input\{([\w\.]+)\}", l)
                if m:
                    log.debug(f"Found matching line: {l}")
                    n = m.group(1)
                    n = n+".tex" if ".tex" not in n else n
                    r += search_for_includes([n])
                else:
                    log.debug(f"Found non-matching line: {l}")
    return r
                    
            
def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="+", help="Files to process")
    parser.add_argument("--list-includes", action="store_true", help="List included files in order")
    parser.add_argument('-v', action='store_true', dest="verbose", help="Be verbose")
    cmdline = parser.parse_args(argv)

    log.basicConfig(level=log.DEBUG if cmdline.verbose else log.WARN)

    if cmdline.list_includes:
        all_files = search_for_includes(cmdline.files)
        print("\n".join(all_files))

if __name__ == "__main__":
    main(sys.argv[1:])
