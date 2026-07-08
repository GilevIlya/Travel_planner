from fastapi import APIRouter, Query

from app.services.art_api import ArtInstituteAPI

router = APIRouter(prefix="/api/v1/artworks", tags=["Artworks"])


@router.get(
    "/search",
    summary="Search artworks in Art Institute Chicago API",
    description="Search for artworks by title/query in the Art Institute of Chicago collection. "
                "Returns a list of matching artworks with their IDs, titles, and artists. "
                "Use the returned `external_id` to add an artwork to a travel project.",
)
async def search_artworks(
    title: str = Query(..., min_length=1, description="Search by title, e.g. 'Sunflowers', 'Mona Lisa'"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=50, description="Results per page"),
):
    results = await ArtInstituteAPI.search_artworks(query=title, page=page, limit=limit)
    return results