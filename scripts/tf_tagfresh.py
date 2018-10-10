#!/usr/bin/env python

import os
import sys
import re
import subprocess
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-d", "--directory", dest="directory", help="(Optional) Where to start the check from. Default is \"./\"")
parser.add_option("-p", "--private-repos", dest="private_repos", help="Space separated list of private repos")
parser.add_option("-l", "--levels", dest="levels", help="FIXME: Do not use; WIP -- (Optional) How many levels deep to travel down directory trees. Default is to follow all the turtles")
(options, args) = parser.parse_args()
directory = options.directory if options.directory else "./"
levels = int(options.levels) if options.levels else 10
private_repos = options.private_repos.split() if options.private_repos else []

def grep_sources(directory):
    regx = re.compile("\s*source\s*=\s*(?:\"|\')(?:https\:\/\/|git\:\:ssh\:\/\/(?:git\@)?)?(?!\.\.|\/)(.*)(?:\"|\')")
    files_sources_dict = {}

    for root, dirs, fnames in os.walk(directory):
        # FIXME: This doesn't work, seems to skip in the wrong place, so ends up
        #        skipping first level too
        if root[len(directory) + 1:].count(os.sep) > levels:
            pass
        else:
            for fname in fnames:
                if fname.endswith(".tf"):
                    this_path = os.path.join(root, fname)

                    with open(this_path) as f:
                        lines = f.readlines()
                        
                        for line in lines:
                            if regx.match(line):
                                m = regx.match(line)
                                m = re.sub(r"(?:git::)(?:ssh://|https://|http://)(?:git\@)*", "", m.group(1))

                                protocol = "https://"
                                for repo in private_repos:
                                    if repo in m:
                                        protocol = "ssh://git@"
                                m = protocol + m

                                if not this_path in files_sources_dict:
                                    files_sources_dict[this_path] = [m]
                                else:
                                    files_sources_dict[this_path].append(m)
                    f.close()

    return files_sources_dict

def check_source(source, this_file):
    if "?ref=" not in source:
        return

    # FIXME: Make ".git?" optional, without entering into the previous capture
    capture_tags_regx = re.compile("(ssh:\/\/.*|https:\/\/.*)(?:\?)?(?:ref\=)(.*)")
    parsed_source = capture_tags_regx.match(source)
    try:
        # TODO: This is horrible. Blame Farid.
        stripped_url = parsed_source.group(1)
        stripped_url = stripped_url.replace(".git", "")
        stripped_url = stripped_url.replace("?", "")
        current_tag = parsed_source.group(2)
    except:
        print("Regexp error for source: " + source)

    remote_tags = []
    strip_refs_regx = re.compile("[a-f0-9]{40}\s*refs\/tags\/([^\\\^]+)(\\n|\^\{\}\\n)")
    p = subprocess.Popen("git ls-remote " + stripped_url, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
        if strip_refs_regx.match(line):
            this_tag = strip_refs_regx.match(line).group(1)
            remote_tags.append(this_tag)

    if sorted(remote_tags)[-1] > current_tag:
        return "WARNING: For source " + stripped_url + " in file " + this_file + "\nLatest = " + sorted(remote_tags)[-1] + ", version used = " + current_tag + "\n"

def check_files(files_to_check):
    stale_sources = []

    for f, sources in files_to_check.iteritems():
        for s in sources:
            stale_source = check_source(s, f)
            if stale_source is not None:
                print(stale_source)
                stale_sources.append(stale_source)

    if len(stale_sources) is not 0:
        print("Stale sources were discovered")
        sys.exit(1)


check_files(grep_sources(directory))