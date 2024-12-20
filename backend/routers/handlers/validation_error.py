from pydantic_core import ValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse

async def validation_error_handler(_: Request, exc: ValidationError) -> JSONResponse:
    ''' Personalize response when ValidationError '''
    return JSONResponse({"error": "Validation Error", "errors": exc.errors()}, status_code=422)