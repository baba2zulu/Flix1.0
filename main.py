from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fzmovies_api import Search, Navigate, DownloadLinks
import requests
import uvicorn
import os

app = FastAPI(title="KrioFlix Aggregator Engine")

# Configure CORS to allow your Lovable app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TMDB_API_KEY = "85b34b408692ca3f88f7b64904349e12"

@app.get("/")
async def root():
    return {"status": "KrioFlix API is online and fetching realtime feeds"}

@app.get("/api/trending")
async def get_trending():
    """Fetches high-res metadata from TMDb to fill the app library."""
    try:
        url = f"https://api.themoviedb.org/3/trending/movie/week?api_key={TMDB_API_KEY}"
        return requests.get(url).json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/search")
async def search_movies(q: str):
    """Enables search for millions of movies via TMDb."""
    try:
        url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={q}"
        return requests.get(url).json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/resolve")
async def resolve_movie(tmdb_id: str, title: str):
    """
    Constructs a list of movie resources exactly like 123movienow.cc
    providing fallbacks to prevent 404 content errors.
    """
    sources =
    
    # Source 1: FzMovies (Scraped via title for small mobile files)
    try:
        search = Search(query=title)
        if search.all_results.movies:
            target = search.all_results.movies
            movie_page = Navigate(target).results
            link_data = DownloadLinks(movie_page.files).results
            sources.append({
                "name": "FzMovies (Primary)",
                "url": link_data.links,
                "type": "direct",
                "quality": "480p"
            })
    except: pass

    # Source 2: Server Video-Alpha (VidSrc.me Embed)
    sources.append({
        "name": "Server Video-Alpha",
        "url": f"https://vidsrc.me/embed/movie/{tmdb_id}",
        "type": "embed",
        "quality": "720p"
    })

    # Source 3: Server Video-Beta (VidSrc.cc Embed)
    sources.append({
        "name": "Server Video-Beta",
        "url": f"https://vidsrc.cc/v2/embed/movie/{tmdb_id}",
        "type": "embed",
        "quality": "HD"
    })

    # Source 4: 123MovieNow Search Redirect (User requested alternative)
    clean_title = title.replace(" ", "-").lower()
    sources.append({
        "name": "123MovieNow (External)",
        "url": f"https://123movienow.cc/search/{clean_title}",
        "type": "redirect",
        "quality": "HD/Auto"
    })

    return {"resources": sources}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
