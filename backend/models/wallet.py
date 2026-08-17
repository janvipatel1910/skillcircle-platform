from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, computed_field


WELCOME_CREDITS = 10_000


class Wallet(BaseModel):
    """Demo credit wallet belonging to one SkillCircle user."""

    model_config = ConfigDict(
        validate_assignment=True,
        extra="forbid",
    )

    user_id: UUID
    available_credits: int = Field(default=WELCOME_CREDITS, ge=0)
    reserved_credits: int = Field(default=0, ge=0)

    @computed_field
    @property
    def total_credits(self) -> int:
        return self.available_credits + self.reserved_credits

    def reserve(self, amount: int) -> None:
        """Move available credits into the reserved balance."""

        if amount <= 0:
            raise ValueError("Reservation amount must be greater than zero")

        if amount > self.available_credits:
            raise ValueError("Insufficient available credits")

        self.available_credits -= amount
        self.reserved_credits += amount

    def release(self, amount: int) -> None:
        """Return cancelled-task credits to the available balance."""

        if amount <= 0:
            raise ValueError("Release amount must be greater than zero")

        if amount > self.reserved_credits:
            raise ValueError("Insufficient reserved credits")

        self.reserved_credits -= amount
        self.available_credits += amount
