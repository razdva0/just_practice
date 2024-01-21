from app.crud.base import CRUDBase
from app.models.users import User
from app.schemas.users import UserInDB, UserUpdateDB

CRUDUser = CRUDBase[User, UserInDB, UserUpdateDB]
crud_user = CRUDUser(User)
