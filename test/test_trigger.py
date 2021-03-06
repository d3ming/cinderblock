from cinderblock.trigger import Trigger
from cinderblock import icinderblock
from zope.interface.verify import verifyObject
import pytest


class FakeCircleCIClient(object):
    def __init__(self, api_token):
        self._builds_triggered = []
        self.api_token = api_token

        class FakeBuild(object):
            @staticmethod
            def trigger(username, project, branch, **build_params):
                self._builds_triggered.append((
                    username, project, branch, build_params))

        self.build = FakeBuild()

fake_api_key = 'api_key'


@pytest.fixture
def trigger():
    return Trigger(fake_api_key, CircleClient=FakeCircleCIClient)


@pytest.fixture
def circleci_client(api):
    return FakeCircleCIClient()


def test_api_key(trigger):
    assert trigger.circleci_client.api_token == fake_api_key


def test_interface(trigger):
    verifyObject(icinderblock.ITrigger, trigger)


def test_trigger_circleci_build(trigger):
    trigger.trigger_circleci_build(
        target_owner='target_owner',
        target_repo='target_repo',
        target_branch='target_branch',
        source_build='source/build/42',
        source_commit='source/commit/12345678deadbeef')

    circleci_client = trigger.circleci_client
    assert len(circleci_client._builds_triggered) == 1

    build = circleci_client._builds_triggered[0]
    username, project, branch, build_params = build

    assert username == 'target_owner'
    assert project == 'target_repo'
    assert branch == 'target_branch'

    assert build_params == {
        'CINDERBLOCK_SOURCE_BUILD': 'source/build/42',
        'CINDERBLOCK_SOURCE_COMMIT': 'source/commit/12345678deadbeef',
        'CINDERBLOCK_CIRCLE_API_TOKEN': fake_api_key
    }


def test_trigger_circleci_build_output_url(trigger, capsys):
    '''trigger_circleci_build prints a URL for the triggered build.'''
    trigger.trigger_circleci_build(
        target_owner='target_owner',
        target_repo='target_repo',
        target_branch='target_branch',
        source_build=None,
        source_commit=None)

    url = 'https://www.circleci.com/gh/%s/%s/tree/%s\n' % (
        'target_owner', 'target_repo', 'target_branch')
    expected = 'Build triggered at ' + url

    out, _ = capsys.readouterr()
    assert out == expected
