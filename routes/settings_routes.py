import state
from fastapi import APIRouter
from pydantic import BaseModel
from utils.api_helpers import resolve_operation, safe_execute

router = APIRouter(
    prefix="/settings",
    tags=["Settings"],
)

#request models
class UpdateSettingsRequest(BaseModel):
    category: str
    setting: str
    value: str | int | float | bool

#routes
@router.post("/update")
def update_settings_endpoint(request: UpdateSettingsRequest):
    safe_execute(
        state.update_settings,
        request.category,
        request.setting,
        request.value
    )

    return {
        "message": "Setting updated successfully",
        "category": request.category,
        "setting": request.setting,
        "value": state.settings[request.category][request.setting]
    }

@router.post("/reset")
def reset_settings_endpoint():
    state.reset_settings()

    return {
        "message": "Settings reset to default",
        "settings": state.settings
    }



