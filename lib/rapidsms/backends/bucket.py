#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4


from .base import BackendBase


class BucketBackend(BackendBase):

    def __init__(self, *args, **kwargs):
        self.bucket = []
        super(BucketBackend, self).__init__(*args, **kwargs)

    def start(self):
        BackendBase.start(self)

    def receive(self, identity, text):
        msg = self.message(identity, text)
        #self.router.incoming_message(msg)
        self.bucket.append(msg)
        return msg

    def send(self, msg):
        self.bucket.append(msg)
        return True
