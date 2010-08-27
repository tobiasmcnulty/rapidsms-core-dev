from nose.tools import assert_equals, assert_true

from django.http import HttpRequest, HttpResponse
from django.test.client import Client
from django.core.urlresolvers import reverse

from rapidsms.tests.harness import MockRouter
from rapidsms.backends.http import RapidHttpBacked


class NewBackend(RapidHttpBacked):
    def configure(self, *args, **kwargs):
        self.username = kwargs.pop('username')
        super(NewBackend, self).configure(*args, **kwargs)


def test_handle_request():
    """ handle_request must return a HttpResponse """
    backend = RapidHttpBacked(name='test')
    response = backend.handle_request(HttpRequest())
    assert_true(isinstance(response, HttpResponse))


def test_extra_config():
    """ Allow custom configuration """
    router = MockRouter()
    backend = NewBackend(name='test', username='rapidsms')
    assert_equals('rapidsms', backend.username)

# new tests below:

def test_handle_message():
    c = Client()
 #   url = reverse('handle_message')
    payload = {'identity': '12345', 'text': 'my test message'}
    response = c.post('/handle-message/', payload)
    assert_equals(response.status_code, 200)
