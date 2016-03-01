#!/usr/bin/python
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
            "context": "paperg/integration",
            "description": "paperg/integration: " + state,
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
        assert args.target_url, "target-url missing or CINDERBLOCK_TARGET_URL is not set!"
        assert args.token, "github token missing or CINDERBLOCK_GITHUB_TOKEN is not set!"
        assert args.user, "github user missing or CINDERBLOCK_GITHUB_USER is not set!"
        assert args.commit, "commit missing or CINDERBLOCK_SHA is not set!"
        assert args.repo, "repo missing or CINDERBLOCK_PROJECT_NAME is not set!"
    except AssertionError as error:
        # Print error/help but don't exit with error since it could be expected
        argparser.print_help()
        print(error)
        sys.exit()


def __parse_args():
    argparser = argparse.ArgumentParser()

    argparser.add_argument('-s', '--state', required=True, default=None,
                           help='State: [success | failure | pending ]')
    argparser.add_argument('-t', '--target-url',
                           default=os.environ.get('CINDERBLOCK_TARGET_URL'),
                           help='target_url for the commit status')
    argparser.add_argument('-u', '--user',
                           default=os.environ.get('CINDERBLOCK_GITHUB_USER'),
                           help='The GitHub user to send commitstatus to')
    argparser.add_argument('-T', '--token',
                           default=os.environ.get('CINDERBLOCK_GITHUB_TOKEN'),
                           help='GitHub API token')
    argparser.add_argument('-c', '--commit', default=os.environ.get('CINDERBLOCK_SHA'),
                           help='The git commit SHA to post status to')
    argparser.add_argument('-r', '--repo',
                           default=os.environ.get('CINDERBLOCK_PROJECT_NAME'),
                           help='The GitHub repo')
    args = argparser.parse_args()
    return args


def main():
    args = __parse_args()
    post_github_commit_status(commit_sha=args.commit, state=args.state,
                              repo=args.repo, user=args.user, token=args.token,
                              target_url=args.target_url)


if __name__ == '__main__':
    main()
