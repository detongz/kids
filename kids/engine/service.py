# coding: utf-8

import collections
import datetime
import os

from oslo_log import log as logging
from oslo_service import service
from osprofiler import profiler

LOG = logging.getLogger(__name__)


class EngineListener(service.Service):
    def __init__(self, hots, topic):
        super(EngineListener, self).__init__()
        self.host = host
        self.topic = topic

    def start(self):
        super(EngineListener, self).start()

    def stop(self):
        super(EngineListener, self).stop()

    def reset(self):
        super(EngineListener, self).reset()

    def wait(self):
        super(EngineListener, self).wait()
