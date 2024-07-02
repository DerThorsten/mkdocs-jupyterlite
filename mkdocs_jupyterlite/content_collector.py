from __future__ import annotations

from collections import defaultdict

from .singleton import Singleton


@Singleton
class ContentCollector:
    def __init__(self):
        self.per_env_content = defaultdict(list)

    def add(self, env, path, content):

        self.per_env_content[env].append({'path': path, 'content': content})


def content_collector():
    return ContentCollector.instance()
