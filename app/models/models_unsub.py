from pydantic import BaseModel
from pydantic import Field

from .base_models import APIResponse


# POST
class POSTUnsubResponse(APIResponse):
    result: dict = Field({}, example={'code': 200, 'error_msg': '', 'result': 'success'})


class POSTUnsub(BaseModel):
    username: str
    notification_id: int
