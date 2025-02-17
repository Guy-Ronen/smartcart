from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from smart_cart.models.receipt import Receipt


class User(SQLModel, table=True):  # type: ignore
    user_id: str = Field(primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str = Field(min_length=8)
    first_name: str = Field(min_length=2)
    last_name: str = Field(min_length=2)
    created_at: int
    updated_at: Optional[int] = None
    last_login: Optional[int] = None
    is_active: bool = Field(default=True, index=True)
    is_superuser: bool = Field(default=False)
    is_staff: bool = Field(default=False)

    receipts: List["Receipt"] = Relationship(back_populates="user")

    @classmethod
    def from_model(cls, item: dict) -> "User":
        return cls(
            user_id=item["user_id"],
            email=item["email"],
            hashed_password=item["hashed_password"],
            first_name=item["first_name"],
            last_name=item["last_name"],
            created_at=item["created_at"],
            updated_at=item.get("updated_at"),
            last_login=item.get("last_login"),
            is_active=item["is_active"],
            is_superuser=item["is_superuser"],
            is_staff=item["is_staff"],
        )
