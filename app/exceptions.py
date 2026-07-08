from fastapi import HTTPException, status


class ProjectNotFoundError(HTTPException):
    def __init__(self, project_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with id {project_id} not found",
        )


class PlaceNotFoundError(HTTPException):
    def __init__(self, place_id: int, project_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Place with id {place_id} not found in project {project_id}",
        )


class ProjectHasVisitedPlacesError(HTTPException):
    def __init__(self, project_id: int):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Project {project_id} has visited places and cannot be deleted",
        )


class ProjectPlaceLimitError(HTTPException):
    def __init__(self, project_id: int, limit: int = 10):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Project {project_id} already has {limit} places (maximum)",
        )


class DuplicatePlaceError(HTTPException):
    def __init__(self, name: str, project_id: int):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Place '{name}' already exists in project {project_id}",
        )


class ArtworkNotFoundError(HTTPException):
    def __init__(self, external_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Artwork with external ID {external_id} not found in Art Institute Chicago API",
        )
