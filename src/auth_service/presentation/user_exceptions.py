from fastapi import status, HTTPException

UserAlreadyExistsError409 = HTTPException(
    status_code=status.HTTP_409_CONFLICT, detail="user already exists"
)

UserFieldError409 = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="username or password is invalid",
)

UserNoFoundError404 = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="user not found"
)
