from typing import TypedDict ,List , Dict

class ResearchState(TypedDict):
    query: str
    paper_urls: List[str]
    summaries: List[Dict]
    contradictions: List[Dict]
    synthesis: str
    status: str
    retry_count: int 
    error_log: List[str]
    timestamp: str