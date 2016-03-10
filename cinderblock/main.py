#!/usr/bin/python
import trigger
import os

'''
Cinderblock - CircleCI workflow for multiple GitHub repos
'''

import argparse

def __parse_args():
    argparser = argparse.ArgumentParser(description=__doc__)

    subparsers = argparser.add_subparsers(dest='action')
    trigger_parser = subparsers.add_parser('trigger',
        help='Triggers a cinderblock job')

    """TODO
    recieve_parser = subparsers.add_parser('receive',
        help='Receives a cinderblock job')
    recieve_args = __parse_receive_args(recieve_parser)
    """

    args = argparser.parse_args()
    if (args.action == 'trigger'):
        trigger_args = __parse_trigger_args(trigger_parser)
        print('trigger with args: {}'.format())
        trigger.main(trigger_args)

    return args

def __parse_receive_args():
    argparser = argparse.ArgumentParser(description=__doc__)

    argparser.add_argument('-s', '--state', default=None, required=True,
                           help='State: [success | failure | pending]')
    argparser.add_argument('-t', '--target-url',
                           default=os.environ.get('CIRCLE_BUILD_URL'),
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

    # Context of the commit status shows info about the integration project
    # Prepend the github_user to distinguish it more
    integration_repo = os.environ.get('CIRCLE_PROJECT_REPONAME')
    args.context = "{}/{}".format(args.github_user, integration_repo)

    args.github_token = os.environ.get('CINDERBLOCK_GITHUB_TOKEN')
    return args


def __parse_trigger_args(argparser):
    argparser.add_argument(
        '-o', '--repo-owner', default=os.environ.get('CINDERBLOCK_REPO_OWNER'))
    argparser.add_argument(
        '-i', '--integration-repo',
        default=os.environ.get('CINDERBLOCK_INTEGRATION_REPO'))
    argparser.add_argument(
        '-b', '--branch', default='master')

    args = argparser.parse_args()
    args.circle_api_token = os.environ.get('CIRCLE_API_TOKEN')
    args.circle_build_num = os.environ.get('CIRCLE_BUILD_NUM')
    args.circle_sha1 = os.environ.get('CIRCLE_SHA1')
    args.circle_build_url = os.environ.get('CIRCLE_BUILD_URL')
    args.circle_project_reponame = os.environ.get('CIRCLE_PROJECT_REPONAME')
    return args


def main():
    args = __parse_args()


main()
