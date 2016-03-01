#!/usr/bin/python

# Script to trigger integration tests from the template-service repo
# Requirements:
# pip install circleclient

import argparse
import os
from circleclient import circleclient


def main():
    args = __parse_args()
    client = circleclient.CircleClient(args.token)

    # Trigger a parametized build with the integration project with
    # env variables to identify the trigger project and the version
    client.build.trigger(args.owner, 'integration', args.branch,
                         CINDERBLOCK_REPO_OWNER=args.owner,
                         CINDERBLOCK_PROJECT_NAME=args.reponame,
                         CINDERBLOCK_SHA=args.commit,
                         CINDERBLOCK_BUILD_NUMBER=args.build,
                         CINDERBLOCK_TARGET_URL=args.build_url)
    print('Triggered integration for {} at commit: {}'.format(
        args.reponame, args.commit))


def __validate_args(args, argparser):
    try:
        assert args.owner, \
            "No owner specified or CINDERBLOCK_REPO_OWNER is not set!"
        assert args.integration_repo, \
            "No integration_repo specified or CINDERBLOCK_INTEGRATION_REPO is not set!"
        assert args.token, "No token specified or CIRCLE_API_TOKEN is not set!"
        assert args.reponame, \
            "No reponame specified or CIRCLE_PROJECT_REPONAME is not set!"
        assert args.commit, "No commit specified or CIRCLE_SHA1 is not set!"
        assert args.build, "No build number specified or CIRCLE_BUILD_NUMBER is not set!"
    except AssertionError as error:
        argparser.print_help()
        raise error


def __parse_args():
    """ Parse commandline args and set defaults based on env variables from CircleCI:
        See https://circleci.com/docs/environment-variables for reference
    """
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-t', '--token', default=os.environ.get('CIRCLE_API_TOKEN'),
                           help='CircleCI API token')
    argparser.add_argument(
        '-o', '--owner', default=os.environ.get('CINDERBLOCK_REPO_OWNER'))
    argparser.add_argument(
        '-i', '--integration-repo',
        default=os.environ.get('CINDERBLOCK_INTEGRATION_REPO'))
    argparser.add_argument(
        '-b', '--branch', default='master')

    args = argparser.parse_args()
    args.build = os.environ.get('CIRCLE_BUILD_NUM')
    args.commit = os.environ.get('CIRCLE_SHA1')
    args.build_url = os.environ.get('CIRCLE_BUILD_URL')
    args.reponame = os.environ.get('CIRCLE_PROJECT_REPONAME')
    __validate_args(args, argparser)
    return args


if __name__ == '__main__':
    main()
