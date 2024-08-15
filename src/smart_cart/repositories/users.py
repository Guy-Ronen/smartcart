from pydantic import BaseModel
from pynamodb.attributes import NumberAttribute, UnicodeAttribute
from pynamodb.models import Model

from smart_cart.schemas.user import User as UserModel
from smart_cart.utils.settings import settings


class User(Model):
    class Meta:
        table_name = settings.table_name
        region = settings.region
        aws_access_key_id = settings.aws_access_key_id
        aws_secret_access_key = settings.aws_secret_access_key
        aws_session_token = settings.aws_session_token
        host = settings.host

    user_id = UnicodeAttribute(hash_key=True)
    username = UnicodeAttribute()
    email = UnicodeAttribute()
    hashed_password = UnicodeAttribute()
    first_name = UnicodeAttribute()
    last_name = UnicodeAttribute()
    created_at = NumberAttribute()
    updated_at = NumberAttribute(null=True)
    last_login = NumberAttribute(null=True)
    is_active = UnicodeAttribute()
    is_superuser = UnicodeAttribute()
    is_staff = UnicodeAttribute()

    @classmethod
    def from_entity(cls, model: UserModel):
        return cls(
            user_id=model.user_id,
            username=model.username,
            email=model.email,
            hashed_password=model.hashed_password,
            first_name=model.first_name,
            last_name=model.last_name,
            created_at=model.created_at,
            updated_at=model.updated_at,
            last_login=model.last_login,
            is_active=model.is_active,
            is_superuser=model.is_superuser,
            is_staff=model.is_staff,
        )


class UserRepository(BaseModel):
    table_name: str
    region: str
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_session_token: str
    host: str

    @staticmethod
    def create_user(user: UserModel):
        item = User.from_entity(user)
        item.save()

    @staticmethod
    def get_user(user_id: str) -> UserModel | None:
        try:
            item = User.get(hash_key=user_id)
        except User.DoesNotExist:
            return None
        return UserModel.from_dynamoItem(item.to_simple_dict())
