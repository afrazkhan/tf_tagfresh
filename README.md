# Terraform TagFresh

Simple script to scan `source` lines in your Terraform code and check that you're
using the latest tags for those sources.

This is my first Python thing, so use at your own risk :D It will currently traverse
down all directories looking for `.tf` files, and query the sources it finds. You
may end up making a great many SSH calls.

## Usage

Run it in the directory you want to check, or supply a directory with `-d`.

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
      -p "git.fantastico.com", --private-repos="git.fantastico.com"
                            (Optional) Space separated list of private repos
      -l LEVELS, --levels=LEVELS
                            (Optional) How many levels deep to travel down
                            directory trees. Default is to follow all the turtles

## Gitlab CI

One of the most common ways in which you want to use this is in a CI/CD pipeline. 
Here's some sample code for a gitlab CI pipeline:

```
test_tf_tag_sources:
  image: "python:2.7.15"
  before_script:
    - 'which ssh-agent || ( apt-get update -y && apt-get install openssh-client -y )'
    - eval $(ssh-agent -s)
    - echo "$SSH_KEY" | tr -d '\r' | ssh-add - > /dev/null
    - mkdir -p ~/.ssh
    - echo "StrictHostKeyChecking=no" > ~/.ssh/config
    - chmod -R 700 ~/.ssh
  script:
    - pip install git+git://github.com/afrazkhan/tf_tagfresh
    - tf_tagfresh.py -p gitlab.example.com
  allow_failure: true
```

The above snippet expects a GitLab secret variable called `SSH_KEY`, that contains a private key able to access all repositories listed in the `--private-repos` flag.
