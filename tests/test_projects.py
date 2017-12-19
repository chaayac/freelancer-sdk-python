from freelancersdk.session import Session
from freelancersdk.resources.projects import (
    create_project, create_hourly_project, create_hireme_project,
    create_local_project,
    get_projects, search_projects,
    place_project_bid, get_bids, award_project_bid, revoke_project_bid,
    accept_project_bid, retract_project_bid, highlight_project_bid,
    create_milestone_payment, release_milestone_payment,
    request_release_milestone_payment, cancel_milestone_payment,
    create_milestone_request, accept_milestone_request,
    reject_milestone_request, delete_milestone_request,
    get_jobs
)
from freelancersdk.resources.projects.helpers import (
    create_budget_object, create_currency_object, create_job_object,
    create_hourly_project_info_object, create_country_object,
    create_location_object, create_bid_object, create_get_projects_object,
    create_get_projects_project_details_object,
    create_get_projects_user_details_object
)
from freelancersdk.resources.projects.types import MilestoneReason
try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock

import unittest


class FakeProjectPostResponse:

    status_code = 200

    def json(self):
        return {
            'result': {
                'title': 'My New Project',
                'seo_url': 'java/foo',
            }
        }


class FakeGetProjectsGetResponse:

    status_code = 200

    def json(self):
        return {
            'status': 'success',
            'result': {
                'total_count': 3,
                'selected_bids': None,
                'users': {
                    '101': {
                        'id': '101',
                        'username': 'user1',
                    },
                    '102': {
                        'id': '101',
                        'username': 'user2',
                    },
                    '103': {
                        'id': '101',
                        'username': 'user3',
                    },
                },
                'projects': [
                    {
                        'id': '201',
                        'title': 'Phasellus blandit posuere enim',
                        'description': 'Morbi libero elit, posuere eu suscipit'
                        ' et dignissim non urna.',
                    },
                    {
                        'id': '202',
                        'title': 'Donec fringilla elit velit',
                        'description': 'Vestibulum mauris risus, molestie vel'
                        ' velit a, semper ultricies odio.',
                    },
                    {
                        'id': '203',
                        'title': 'In hac habitasse platea dictumst',
                        'description': 'Duis sed tristique urna.'
                        ' Nullam vestibulum elit at quam dapibus venenatis.',
                    },
                ],
            },
        }


class FakeSearchProjectsGetResponse:

    status_code = 200

    def json(self):
        return {
            'status': 'success',
            'result': {
                'total_count': 1000,
                'selected_bids': [],
                'users': [],
                'projects': [
                    {
                        'id': '201',
                        'title': 'Phasellus blandit posuere enim',
                        'description': 'Morbi libero elit, posuere eu suscipit'
                        ' logo et dignissim non urna.',
                    },
                    {
                        'id': '202',
                        'title': 'Donec fringilla elit velit',
                        'description': 'Vestibulum mauris risus, molestie logo'
                        ' vel velit a, semper ultricies odio.',
                    },
                    {
                        'id': '203',
                        'title': 'In hac habitasse platea dictumst',
                        'description': 'Duis sed tristique urna. Nullam'
                        ' vestibulum elit at quam dapibus logo venenatis.',
                    },
                ],
            },
        }


class FakePlaceBidPostResponse:

    status_code = 200

    def json(self):
        return {
            'result': {
                'milestone_percentage': 100,
                'period': 2,
                'id': 39343812,
                'retracted': False,
                'project_owner_id': 12,
                'submitdate': 1424142980,
                'project_id': 1,
                'bidder_id': 2,
                'description': 'A bid',
                'time_submitted': 1424142980,
                'amount': 10
            }
        }


class FakeGetBidsGetResponse:

    status_code = 200

    def json(self):
        return {
            'status': 'success',
            'result': {
                'bids': [
                    {
                        'id': 301,
                        'project_id': 201,
                        'bidder_id': 101,
                    },
                    {
                        'id': 302,
                        'project_id': 201,
                        'bidder_id': 102,
                    },
                    {
                        'id': 303,
                        'project_id': 201,
                        'bidder_id': 103,
                    },
                    {
                        'id': 304,
                        'project_id': 202,
                        'bidder_id': 104,
                    },
                    {
                        'id': 305,
                        'project_id': 202,
                        'bidder_id': 105,
                    },
                ],
                'users': None,
                'projects': None,
            },
        }


class FakeAwardBidPutResponse:

    status_code = 200

    def json(self):
        return {
            'status': 'success'
        }


class FakeRevokeBidPutResponse:

    status_code = 200

    def json(self):
        return {
            'status': 'success'
        }


class FakeAcceptBidPutResponse:

    status_code = 200

    def json(self):
        return {
            'status': 'success'
        }


class FakeRetractBidPutResponse:

    status_code = 200

    def json(self):
        return {
            'status': 'success'
        }


class FakeHighlightBidPutResponse:

    status_code = 200

    def json(self):
        return {
            'status': 'success'
        }


class FakeMilestonePaymentCreatePostResponse:

    status_code = 200

    def json(self):
        return {
            'result': {
                'bidder_id': 2,
                'description': 'A milestone',
                'time_submitted': 1424142980,
                'amount': 10,
                'reason': MilestoneReason.PARTIAL_PAYMENT,
            }
        }


class FakeMilestonePaymentReleasePutResponse:

    status_code = 200

    def json(self):
        return {
            'status': 'success'
        }


class FakeCreateMilestoneRequestPostResponse:

    status_code = 200

    def json(self):
        return {
            'result': {
                'project_id': 1,
                'bid_id': 1,
                'amount': 10,
                'description': 'This is a milestone request'
            }
        }


class FakeAcceptMilestoneRequestPutResponse:

    status_code = 200

    def json(self):
        return {
            'status': 'success'
        }


class FakeRejectMilestoneRequestPutResponse:

    status_code = 200

    def json(self):
        return {
            'status': 'success'
        }


class FakeDeleteMilestoneRequestPutResponse:

    status_code = 200

    def json(self):
        return {
            'status': 'success'
        }


class FakeGetJobsGetResponse:

    status_code = 200

    def json(self):
        return {
            'status': 'success',
            'result': [
                {
                    'id': 20,
                    'name': 'Graphic Design',
                    'seo_url': 'graphic-design',
                    'seo_info': {},
                },
                {
                    'id': 32,
                    'name': 'Logo Design',
                    'seo_url': 'logo-design',
                    'seo_info': {},
                },
            ],
        }


class TestProjects(unittest.TestCase):
    def setUp(self):
        self.session = Session(oauth_token='$sometoken', url='https://fake-fln.com')

    def tearDown(self):
        pass

    def test_create_project(self):
        project_data = {
            'title': 'My new project',
            'description': 'description',
            'currency': create_currency_object(id=1),
            'budget': create_budget_object(minimum=10),
            'jobs': [create_job_object(id=7)],
        }

        self.session.session.post = Mock()
        self.session.session.post.return_value = FakeProjectPostResponse()
        p = create_project(self.session, **project_data)
        self.session.session.post.assert_called_once_with(
            'https://fake-fln.com/api/projects/0.1/projects/',
            json=project_data,
            verify=True)
        self.assertEquals(p.url, 'https://fake-fln.com/projects/java/foo')

    def test_create_hourly_project(self):
        project_data = {
            'title': 'My new hourly project',
            'description': 'description',
            'currency': create_currency_object(id=1),
            'budget': create_budget_object(minimum=10),
            'jobs': [create_job_object(id=7)],
            'hourly_project_info':
                create_hourly_project_info_object(commitment_hours=40,
                                                  commitment_interval='WEEK')
        }

        self.session.session.post = Mock()
        self.session.session.post.return_value = FakeProjectPostResponse()
        p = create_hourly_project(self.session, **project_data)
        project_data.update(type='HOURLY')
        self.session.session.post.assert_called_once_with(
            'https://fake-fln.com/api/projects/0.1/projects/',
            json=project_data,
            verify=True)
        self.assertEquals(p.url, 'https://fake-fln.com/projects/java/foo')

    def test_create_hireme_project(self):
        project_data = {
            'title': 'My new project',
            'description': 'description',
            'currency': create_currency_object(id=1),
            'budget': create_budget_object(minimum=10),
            'jobs': [create_job_object(id=1)],
            'hireme_initial_bid': create_bid_object(id=None, bidder_id=2,
                                                    project_id=None,
                                                    retracted=None,
                                                    amount=100, period=7,
                                                    description='Hello',
                                                    project_owner_id=1)
        }

        self.session.session.post = Mock()
        self.session.session.post.return_value = FakeProjectPostResponse()
        p = create_hireme_project(self.session, **project_data)
        project_data.update(hireme=True)
        self.session.session.post.assert_called_once_with(
            'https://fake-fln.com/api/projects/0.1/projects/',
            json=project_data,
            verify=True)
        self.assertEquals(p.url, 'https://fake-fln.com/projects/java/foo')

    def test_create_local_project(self):
        project_data = {
            'title': 'My new local project',
            'description': 'description',
            'currency': create_currency_object(id=1),
            'budget': create_budget_object(minimum=10),
            'jobs': [create_job_object(id=1)],
            'location': create_location_object(
                create_country_object('Australia'),
                'Sydney', -33.875461, 151.201678)
        }

        self.session.session.post = Mock()
        self.session.session.post.return_value = FakeProjectPostResponse()
        p = create_local_project(self.session, **project_data)
        project_data.update(local=True)
        self.session.session.post.assert_called_once_with(
            'https://fake-fln.com/api/projects/0.1/projects/',
            json=project_data,
            verify=True)
        self.assertEquals(p.url, 'https://fake-fln.com/projects/java/foo')

    def test_get_projects(self):
        query = create_get_projects_object(
            project_ids=[
                201,
                202,
                203,
            ],
            project_details=create_get_projects_project_details_object(
                full_description=True,
            ),
            user_details=create_get_projects_user_details_object(
                basic=True,
            ),
        )

        self.session.session.get = Mock()
        self.session.session.get.return_value = FakeGetProjectsGetResponse()
        get_projects(self.session, query)
        self.session.session.get.assert_called_once_with(
            'https://fake-fln.com/api/projects/0.1/projects/',
            params=query,
            verify=True)

    def test_search_projects(self):
        query_data = {
            'query': 'logo',
            'project_types': 'fixed',
            'limit': 3,
            'offset': 0,
            'active_only': True,
        }

        self.session.session.get = Mock()
        self.session.session.get.return_value = FakeSearchProjectsGetResponse()
        p = search_projects(self.session, **query_data)
        del(query_data['active_only'])
        self.session.session.get.assert_called_once_with(
            'https://fake-fln.com/api/projects/0.1/projects/active/',
            params=query_data,
            verify=True)
        self.assertEquals(len(p['projects']), query_data['limit'])

    def test_place_project_bid(self):
        bid_data = {
            'project_id': 1,
            'bidder_id': 2,
            'amount': 10,
            'period': 2,
            'milestone_percentage': 100,
            'description': 'A bid',
        }

        self.session.session.post = Mock()
        self.session.session.post.return_value = FakePlaceBidPostResponse()
        b = place_project_bid(self.session, **bid_data)
        self.session.session.post.assert_called_once_with(
            'https://fake-fln.com/api/projects/0.1/bids/',
            json=bid_data,
            verify=True)
        self.assertTrue(getattr(b, 'bidder_id'))
        self.assertTrue(getattr(b, 'description'))

    def test_get_bids(self):
        get_bids_data = {
            'project_ids': [
                101,
                102,
            ],
            'limit': 20,
            'offset': 10,
        }

        self.session.session.get = Mock()
        self.session.session.get.return_value = FakeGetBidsGetResponse()
        j = get_bids(self.session, **get_bids_data)
        get_bids_data.update({'projects[]': get_bids_data['project_ids']})
        del(get_bids_data['project_ids'])
        self.session.session.get.assert_called_once_with(
            'https://fake-fln.com/api/projects/0.1/bids/',
            params=get_bids_data,
            verify=True)
        self.assertEquals(len(j['bids']), 5)

    def test_award_project_bid(self):
        bid_data = {
            'bid_id': 1,
        }

        self.session.session.put = Mock()
        self.session.session.put.return_value = FakeAwardBidPutResponse()
        award_project_bid(self.session, **bid_data)
        self.session.session.put.assert_called_once_with(
            'https://fake-fln.com/api/projects/0.1/bids/1/',
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            params={'action': 'award'},
            data=None,
            json=None,
            verify=True)

    def test_revoke_project_bid(self):
        bid_data = {
            'bid_id': 1,
        }

        self.session.session.put = Mock()
        self.session.session.put.return_value = FakeRevokeBidPutResponse()
        revoke_project_bid(self.session, **bid_data)
        self.session.session.put.assert_called_once_with(
            'https://fake-fln.com/api/projects/0.1/bids/1/',
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            params={'action': 'revoke'},
            data=None,
            json=None,
            verify=True)

    def test_accept_project_bid(self):
        bid_data = {
            'bid_id': 1,
        }

        self.session.session.put = Mock()
        self.session.session.put.return_value = FakeAcceptBidPutResponse()
        accept_project_bid(self.session, **bid_data)
        self.session.session.put.assert_called_once_with(
            'https://fake-fln.com/api/projects/0.1/bids/1/',
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            params={'action': 'accept'},
            data=None,
            json=None,
            verify=True)

    def test_retract_project_bid(self):
        bid_data = {
            'bid_id': 1,
        }

        self.session.session.put = Mock()
        self.session.session.put.return_value = FakeRetractBidPutResponse()
        retract_project_bid(self.session, **bid_data)
        self.session.session.put.assert_called_once_with(
            'https://fake-fln.com/api/projects/0.1/bids/1/',
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            params={'action': 'retract'},
            data=None,
            json=None,
            verify=True)

    def test_highlight_project_bid(self):
        bid_data = {
            'bid_id': 1,
        }

        self.session.session.put = Mock()
        self.session.session.put.return_value = FakeHighlightBidPutResponse()
        highlight_project_bid(self.session, **bid_data)
        self.session.session.put.assert_called_once_with(
            'https://fake-fln.com/api/projects/0.1/bids/1/',
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            params={'action': 'highlight'},
            data=None,
            json=None,
            verify=True)

    def test_create_milestone_payment(self):
        milestone_data = {
            'project_id': 1,
            'bidder_id': 2,
            'amount': 10,
            'reason': MilestoneReason.PARTIAL_PAYMENT,
            'description': 'This is a milestone',
        }

        self.session.session.post = Mock()
        self.session.session.post.return_value = FakeMilestonePaymentCreatePostResponse()
        m = create_milestone_payment(self.session, **milestone_data)
        self.session.session.post.assert_called_once_with(
            'https://fake-fln.com/api/projects/0.1/milestones/',
            json=milestone_data,
            verify=True)
        self.assertTrue(getattr(m, 'bidder_id'))
        self.assertTrue(getattr(m, 'description'))
        self.assertEquals(m.reason, MilestoneReason.PARTIAL_PAYMENT)

    def test_release_milestone_payment(self):
        milestone_data = {
            'milestone_id': 1,
            'amount': 10,
        }

        self.session.session.put = Mock()
        self.session.session.put.return_value = FakeMilestonePaymentReleasePutResponse()
        release_milestone_payment(self.session, **milestone_data)
        self.session.session.put.assert_called_once_with(
            'https://fake-fln.com/api/projects/0.1/milestones/1/',
            headers=None,
            params={'action': 'release'},
            data=None,
            json={'amount': 10},
            verify=True)

    def test_request_release_milestone_payment(self):
        milestone_data = {
            'milestone_id': 1,
        }

        self.session.session.put = Mock()
        self.session.session.put.return_value = FakeMilestonePaymentReleasePutResponse()
        request_release_milestone_payment(self.session, **milestone_data)
        self.session.session.put.assert_called_once_with(
            'https://fake-fln.com/api/projects/0.1/milestones/1/',
            headers=None,
            params={'action': 'request_release'},
            data=None,
            json=None,
            verify=True)

    def test_cancel_milestone_payment(self):
        milestone_data = {
            'milestone_id': 1,
        }

        self.session.session.put = Mock()
        self.session.session.put.return_value = FakeMilestonePaymentReleasePutResponse()
        cancel_milestone_payment(self.session, **milestone_data)
        self.session.session.put.assert_called_once_with(
            'https://fake-fln.com/api/projects/0.1/milestones/1/',
            headers=None,
            params={'action': 'cancel'},
            data=None,
            json=None,
            verify=True)

    def test_create_milestone_request(self):
        milestone_request_data = {
            'project_id': 1,
            'bid_id': 1,
            'amount': 10,
            'description': 'This is a milestone request',
        }

        self.session.session.post = Mock()
        self.session.session.post.return_value = FakeCreateMilestoneRequestPostResponse()
        m = create_milestone_request(self.session, **milestone_request_data)
        self.session.session.post.assert_called_once_with(
            'https://fake-fln.com/api/projects/0.1/milestone_requests/',
            json=milestone_request_data,
            verify=True)
        self.assertTrue(getattr(m, 'project_id'))
        self.assertTrue(getattr(m, 'bid_id'))
        self.assertTrue(getattr(m, 'amount'))
        self.assertTrue(getattr(m, 'description'))

    def test_accept_milestone_request(self):
        milestone_request_data = {
            'milestone_request_id': 1,
        }

        self.session.session.put = Mock()
        self.session.session.put.return_value = FakeAcceptMilestoneRequestPutResponse()
        accept_milestone_request(self.session, **milestone_request_data)
        self.session.session.put.assert_called_once_with(
            'https://fake-fln.com/api/projects/0.1/milestone_requests/1/',
            headers=None,
            params={'action': 'accept'},
            data=None,
            json=None,
            verify=True)

    def test_reject_milestone_request(self):
        milestone_request_data = {
            'milestone_request_id': 1,
        }

        self.session.session.put = Mock()
        self.session.session.put.return_value = FakeRejectMilestoneRequestPutResponse()
        reject_milestone_request(self.session, **milestone_request_data)
        self.session.session.put.assert_called_once_with(
            'https://fake-fln.com/api/projects/0.1/milestone_requests/1/',
            headers=None,
            params={'action': 'reject'},
            data=None,
            json=None,
            verify=True)

    def test_delete_milestone_request(self):
        milestone_request_data = {
            'milestone_request_id': 1,
        }

        self.session.session.put = Mock()
        self.session.session.put.return_value = FakeDeleteMilestoneRequestPutResponse()
        delete_milestone_request(self.session, **milestone_request_data)
        self.session.session.put.assert_called_once_with(
            'https://fake-fln.com/api/projects/0.1/milestone_requests/1/',
            headers=None,
            params={'action': 'delete'},
            data=None,
            json=None,
            verify=True)

    def test_get_jobs(self):
        get_jobs_data = {
            'job_ids': [
                20,
                32,
            ],
            'seo_details': True,
            'lang': 'en',
        }

        self.session.session.get = Mock()
        self.session.session.get.return_value = FakeGetJobsGetResponse()
        j = get_jobs(self.session, **get_jobs_data)
        get_jobs_data.update({'jobs[]': get_jobs_data['job_ids']})
        del(get_jobs_data['job_ids'])
        self.session.session.get.assert_called_once_with(
            'https://fake-fln.com/api/projects/0.1/jobs/',
            params=get_jobs_data,
            verify=True)
        self.assertEquals(len(j), len(get_jobs_data['jobs[]']))
