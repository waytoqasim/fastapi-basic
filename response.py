def success_response(message: str, data=None):
    return {"success": True, "message": message, "data": data}


def error_response(message: str, status_code: int = 400):
    from fastapi import HTTPException
    raise HTTPException(
        status_code=status_code,
        detail={
            "success": False,
            "message": message,
            "data": None
        }
    )
