from fastapi import APIRouter
import state

router = APIRouter(
    prefix="/history",
    tags=["History"]
)


@router.get("/")
def get_history_endpoint():
    return {
        "history": state.get_history()
    }

@router.get("/summary")
def history_summary():
    history = state.get_history()

    summary = []

    for i, entry in enumerate(history):
        summary.append({
            "index": i,
            "display_name": entry["display_name"]
        })

    return {"history": summary}

@router.get("/{index}")
def get_history_entry_endpoint(index: int):
    return state.get_history_entry(index)


@router.delete("/{index}")
def delete_history_entry_endpoint(index: int):
    message = state.delete_history_entry(index)

    return {
        "message": message
    }


@router.post("/clear")
def clear_history_endpoint():
    state.clear_history()

    return {
        "message": "History cleared"
    }


@router.post("/replay/{index}")
def replay_history_endpoint(index: int):
    return state.get_replay_payload(index)