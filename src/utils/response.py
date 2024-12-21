def format_response(status: str, message: str, data: dict = None):
    return {"status": status, "message": message, "data": data}
