# Terraform TagFresh

Simple script to scan `source` lines in your Terraform code and check that you're
using the latest tags for those sources.

This is my first Python thing, so use at your own risk :D It will currently traverse
down all directories looking for `.tf` files, and query the sources it finds. You
may end up making a great many SSH calls.

## Usage

Run it in the directory you want to check, or supply a directory with `-d`. Note:
`--levels` is a work in progress, do not use it :)

The sources to be checked must either be public, or you must have access to them
via an SSH key. Specifiy private repos with the `--private-repos` option as a
space separated list in quotes. Alternatively, you can type your password out
a million times :)

    Usage: tf_tagfresh.py [options]

    Options:
    -h, --help            show this help message and exit
    -d DIRECTORY, --directory=DIRECTORY
                        (Optional) Where to start the check from. Default is
                        "./"
    -p PRIVATE_REPOS, --private-repos=PRIVATE_REPOS
                        Space separated list of private repos
    -l LEVELS, --levels=LEVELS
                        FIXME: Do not use; WIP -- (Optional) How many levels
                        deep to travel down directory trees. Default is to
                        follow all the turtles