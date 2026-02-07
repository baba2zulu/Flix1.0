from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fzmovies_api import Search, Navigate, DownloadLinks
import uvicorn
import os

app = FastAPI(title="KrioFlix Multi-Source Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def health():
    return {"status": "KrioFlix Aggregator is Live"}

@app.get("/api/resolve")
async def resolve_movie(movie_id: str, title: str = "Movie"):
    """
    Attempts to resolve the movie through multiple high-priority sources
    to avoid the 404 'Not Found' error.
    """
    sources =
    
    # Source 1: FzMovies (Best for small files/low data)
    try:
        search = Search(query=movie_id)
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

    # Source 2: 123MovieNow Redirect (User requested alternative)
    # We construct a search redirect for this site
    clean_title = title.replace(" ", "-").lower()
    sources.append({
        "name": "123MovieNow (Alternative)",
        "url": f"https://123movienow.cc/search/{clean_title}",
        "type": "redirect",
        "quality": "HD/Auto"
    })

    # Source 3: VidSrc ME (Reliable Fallback)
    sources.append({
        "name": "Server Video-Alpha",
        "url": f"https://vidsrc.me/embed/movie/{movie_id}",
        "type": "embed",
        "quality": "720p"
    })

    # Source 4: VidSrc CC (Backup)
    sources.append({
        "name": "Server Video-Beta",
        "url": f"https://vidsrc.cc/v2/embed/movie/{movie_id}",
        "type": "embed",
        "quality": "HD"
    })

    return {"movie_id": movie_id, "title": title, "resources": sources}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
