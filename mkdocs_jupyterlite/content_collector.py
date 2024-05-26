from .singleton import Singleton
from collections import defaultdict 


@Singleton
class ContentCollector:
    def __init__(self):
        self.per_env_content = defaultdict(list)

    def add(self, env, path, content):
     
        self.per_env_content[env].append({ "path": path, "content": content})
    

def content_collector():
    return ContentCollector.instance()