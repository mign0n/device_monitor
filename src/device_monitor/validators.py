import uuid
from typing import Any

from fastapi import HTTPException, status

from device_monitor.crud import BaseRepository, ModelType


async def check_object_exists(
    obj_id: uuid.UUID,
    repository: BaseRepository[ModelType],
    detail: Any = "Object not found",
) -> ModelType:
    """Check if an object exists in the database.

    Args:
        obj_id: Object ID.
        repository: The repository used to access database object.
        detail: Any data to be sent to the client in the `detail` key of the
            JSON response.

    Raises:
        HTTPException: If the object with the given identifier is not found,
            a 404 HTTPException is raised with an appropriate error message.

    Returns:
        The Model object if found.
    """
    obj = await repository.get_by_id(obj_id)
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
        )
    return obj
