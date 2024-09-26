from select_topic import SearchTopicsResponse, SearchTopic
from pydantic import BaseModel

class TalkTopic(BaseModel):
    scrape_data: str
    search_topic: SearchTopic

def make_draft(scrape_data, search_topic: SearchTopicsResponse):
    