from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fzmovies_api import Search, Navigate, DownloadLinks
from fzmovies_api.filters import RecentlyReleasedFilter, IMDBTop250Filter
import uvicorn
import os

app = FastAPI(title="KrioFlix Bridge API")

# Update this to allow your Lovable production URL
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For production, you can replace "*" with your specific Lovable domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def health_check():
    return {"status": "KrioFlix API is online"}

@app.get("/api/trending")
async def get_trending():
    try:
        # IMDB Top 250 logic from fzmovies-api
        search = Search(query=IMDBTop250Filter())
        return {"results": search.all_results.movies[:20]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/search")
async def search_movies(q: str):
    try:
        search = Search(query=q)
        return {"results": search.all_results.movies}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/resolve")
async def resolve_movie(movie_id: str):
    """
    Resolves links using fzmovies navigation logic with a fallback.
    """
    try:
        # Search specifically for the ID/Title
        search = Search(query=movie_id)
        if not search.all_results.movies:
            raise ValueError("Movie not found on primary source")
            
        target_movie = search.all_results.movies
        
        # Navigate through the fzmovies mirror pages
        movie_page = Navigate(target_movie).results
        
        # Select quality (Index 0 is typically 480p - best for SL data)
        file_option = movie_page.files 
        
        # Extract metadata and link
        link_data = DownloadLinks(file_option).results
        
        return {
            "title": target_movie.title,
            "stream_url": link_data.links,
            "size": link_data.size,
            "quality": "480p",
            "source": "fzmovies.cms"
        }
    except Exception:
        # FALLBACK: If fzmovies scraping fails, return a VidSrc embed link
        return {
            "fallback_embed": f"https://vidsrc.to/embed/movie/{movie_id}",
            "source": "vidsrc.to (Fallback)",
            "quality": "HD/Auto"
        }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
