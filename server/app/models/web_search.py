from pydantic import BaseModel, Field
from typing import List, Optional


class SearchResultItem(BaseModel):
    title: str = Field(..., description="The title of the search result")
    url: str = Field(..., description="The direct URL to the content")
    snippet: str = Field(..., description="A short summary of the content")


class WebSearchResponse(BaseModel):
    query: str = Field(..., description="The search query executed")
    results: List[SearchResultItem] = Field(
        ..., description="List of top search results"
    )
    summary: str = Field(
        ...,
        description="A concise answer to the user's question based on results",
    )

    
