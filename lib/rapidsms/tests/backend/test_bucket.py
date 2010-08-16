#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4


import sys
import time
import threading
from nose.tools import assert_equals
from ...backends.base import get_backend
from ...backends.bucket import BucketBackend
from ...messages import OutgoingMessage
from ...router import Router


def test_bucket_swallows_messages():
    backend = get_backend("mock", "rapidsms.backends.bucket")
    backend.receive("1234", "Mock Incoming Message")

    msg = object()
    backend.send(msg)

    assert_equals(backend.bucket[0].text, "Mock Incoming Message")
    assert_equals(backend.bucket[1], msg)
    assert_equals(len(backend.bucket), 2)
