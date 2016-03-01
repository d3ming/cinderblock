#!/usr/bin/python

'''
Posts commit status to GitHub

Works together cinderblock.py which will provide commitstatus.py
with default values to use
'''

import requests
import os
import json
import argparse
import sys


def post_github_commit_status(commit_sha, state, repo, user, token,
                              target_url):
    build_number = os.environ.get('CIRCLE_BUILD_NUMBER')
    if build_number:
        target_url += "/{}".format(build_number)
    data = {"state": state,
            "context": "{}}/{}".format(user, repo),
            "description": "{}/{} status: {}".format(user, repo, state),
            "target_url": target_url}
    data_json = json.dumps(data)
    headers = {'Content-Type': 'application/json'}
    url = "https://api.github.com/repos/{}/{}/statuses/{}?access_token={}".format(
        user, repo, commit_sha, token)

    response = requests.post(url, data=data_json, headers=headers)
    print("Posting commit status={} for {}/{}/{} got response:\n{}".format(
        state, user, repo, commit_sha, response.content))
    return response


def __validate_args(args, argparser):
    try:
        assert args.target_url, \
            "target_url missing or CINDERBLOCK_TARGET_URL is not set!"
        assert args.github_token, \
            "github_token missing or CINDERBLOCK_GITHUB_TOKEN is not set!"
        assert args.github_user, \
            "github_user user missing or CINDERBLOCK_GITHUB_USER is not set!"
        assert args.commit_sha, \
            "commit_sha missing or CINDERBLOCK_COMMIT_SHA is not set!"
        assert args.repo_name, \
            "repo_name missing or CINDERBLOCK_REPO_NAME is not set!"
    except AssertionError as error:
        # Print error/help but don't exit with error since it could be expected
        argparser.print_help()
        print(error)
        sys.exit()


def __parse_args():
    argparser = argparse.ArgumentParser(description=__doc__)

    argparser.add_argument('-s', '--state', default=None, required=True,
                           help='State: [success | failure | pending ]')
    argparser.add_argument('-t', '--target-url',
                           default=os.environ.get('CINDERBLOCK_TARGET_URL'),
                           help='target_url for the commit status')
    argparser.add_argument('-u', '--github-user',
                           default=os.environ.get('CINDERBLOCK_GITHUB_USER'),
                           help='The GitHub user to send commitstatus to')
    argparser.add_argument('-c', '--commit-sha',
                           default=os.environ.get('CINDERBLOCK_COMMIT_SHA'),
                           help='The git commit SHA to post status to')
    argparser.add_argument('-r', '--repo-name',
                           default=os.environ.get('CINDERBLOCK_REPO_NAME'),
                           help='The GitHub repo')
    args = argparser.parse_args()
    args.github_token = os.environ.get('CINDERBLOCK_GITHUB_TOKEN')
    __validate_args(args, argparser)
    return args


def main():
    args = __parse_args()
    post_github_commit_status(commit_sha=args.commit_sha, state=args.state,
                              repo=args.repo_name, user=args.github_user,
                              token=args.github_token,
                              target_url=args.target_url)


if __name__ == '__main__':
    main()
