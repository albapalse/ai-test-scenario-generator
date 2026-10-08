from typing import Literal

from pydantic import BaseModel, Field


class TestCase(BaseModel):
    title: str = Field(min_length=3)
    category: Literal["happy path", "negative", "edge case", "accessibility"]
    priority: Literal["high", "medium", "low"]
    preconditions: list[str]
    steps: list[str] = Field(min_length=1)
    expected_result: str = Field(min_length=3)


class TestPlan(BaseModel):
    feature: str = Field(min_length=10)
    test_cases: list[TestCase] = Field(min_length=1)
