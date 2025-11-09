from typing import Any, Optional
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("youtube")

# Constants
YOUTUBE_API_BASE = "https://www.googleapis.com/youtube/v3"
USER_AGENT = "youtube-mcp/1.0"

# You'll need to set your YouTube API key
# Get one from: https://console.cloud.google.com/apis/credentials
YOUTUBE_API_KEY = "Your-api-key"


@mcp.tool()
async def search_videos(
    query: str,
    max_results: int = 10,
    order: str = "relevance"
) -> dict[str, Any]:
    """
    Search for YouTube videos.
    
    Args:
        query: Search query string
        max_results: Maximum number of results to return (1-50, default: 10)
        order: Order of results - relevance, date, rating, title, viewCount (default: relevance)
    
    Returns:
        Dictionary containing search results with video information
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{YOUTUBE_API_BASE}/search",
                params={
                    "part": "snippet",
                    "q": query,
                    "maxResults": min(max_results, 50),
                    "order": order,
                    "type": "video",
                    "key": YOUTUBE_API_KEY
                },
                headers={"User-Agent": USER_AGENT},
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            return {"error": f"HTTP error occurred: {str(e)}"}


@mcp.tool()
async def get_video_details(video_id: str) -> dict[str, Any]:
    """
    Get detailed information about a specific YouTube video.
    
    Args:
        video_id: YouTube video ID
    
    Returns:
        Dictionary containing detailed video information including statistics
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{YOUTUBE_API_BASE}/videos",
                params={
                    "part": "snippet,contentDetails,statistics",
                    "id": video_id,
                    "key": YOUTUBE_API_KEY
                },
                headers={"User-Agent": USER_AGENT},
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            return {"error": f"HTTP error occurred: {str(e)}"}


@mcp.tool()
async def get_channel_info(channel_id: str) -> dict[str, Any]:
    """
    Get information about a YouTube channel.
    
    Args:
        channel_id: YouTube channel ID
    
    Returns:
        Dictionary containing channel information and statistics
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{YOUTUBE_API_BASE}/channels",
                params={
                    "part": "snippet,statistics,contentDetails",
                    "id": channel_id,
                    "key": YOUTUBE_API_KEY
                },
                headers={"User-Agent": USER_AGENT},
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            return {"error": f"HTTP error occurred: {str(e)}"}


@mcp.tool()
async def get_video_comments(
    video_id: str,
    max_results: int = 20,
    order: str = "relevance"
) -> dict[str, Any]:
    """
    Get comments for a YouTube video.
    
    Args:
        video_id: YouTube video ID
        max_results: Maximum number of comments to return (1-100, default: 20)
        order: Order of comments - time, relevance (default: relevance)
    
    Returns:
        Dictionary containing video comments
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{YOUTUBE_API_BASE}/commentThreads",
                params={
                    "part": "snippet",
                    "videoId": video_id,
                    "maxResults": min(max_results, 100),
                    "order": order,
                    "key": YOUTUBE_API_KEY
                },
                headers={"User-Agent": USER_AGENT},
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            return {"error": f"HTTP error occurred: {str(e)}"}


@mcp.tool()
async def get_trending_videos(
    region_code: str = "US",
    category_id: Optional[str] = None,
    max_results: int = 10
) -> dict[str, Any]:
    """
    Get trending YouTube videos for a specific region.
    
    Args:
        region_code: ISO 3166-1 alpha-2 country code (default: US)
        category_id: Optional video category ID to filter by
        max_results: Maximum number of results to return (1-50, default: 10)
    
    Returns:
        Dictionary containing trending videos
    """
    params = {
        "part": "snippet,contentDetails,statistics",
        "chart": "mostPopular",
        "regionCode": region_code,
        "maxResults": min(max_results, 50),
        "key": YOUTUBE_API_KEY
    }
    
    if category_id:
        params["videoCategoryId"] = category_id
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{YOUTUBE_API_BASE}/videos",
                params=params,
                headers={"User-Agent": USER_AGENT},
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            return {"error": f"HTTP error occurred: {str(e)}"}


if __name__ == "__main__":
    # Run the MCP server
    mcp.run()