from app.core.auth import fastapi_users

current_user = fastapi_users.current_user(active=True)
superuser = fastapi_users.current_user(active=True, superuser=True)
