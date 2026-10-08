import json

import pytest

from generator import (
    remove_duplicate_test_cases,
    save_markdown_test_plan,
    save_test_plan,
    validate_feature_description,
)
from models import TestCase as QATestCase
from models import TestPlan as QATestPlan


def make_test_case(title: str) -> QATestCase:
    return QATestCase(
        title=title,
        category="negative",
        priority="high",
        preconditions=["The reset page is open."],
        steps=["Submit an expired reset link."],
        expected_result="The password is not changed.",
    )


def test_short_feature_description_is_rejected() -> None:
    with pytest.raises(ValueError):
        validate_feature_description("Login")


def test_duplicate_titles_are_removed_case_insensitively() -> None:
    plan = QATestPlan(
        feature="Password reset link expiration",
        test_cases=[
            make_test_case("Expired reset link"),
            make_test_case("  expired   RESET link  "),
        ],
    )

    result = remove_duplicate_test_cases(plan)

    assert len(result.test_cases) == 1


def test_plan_is_saved_as_json(tmp_path) -> None:
    plan = QATestPlan(
        feature="Password reset link expiration",
        test_cases=[make_test_case("Expired reset link")],
    )
    output_path = tmp_path / "test-plan.json"

    save_test_plan(plan, output_path)

    saved_data = json.loads(output_path.read_text(encoding="utf-8"))
    assert saved_data["feature"] == "Password reset link expiration"
    assert saved_data["test_cases"][0]["priority"] == "high"


def test_plan_is_saved_as_readable_markdown(tmp_path) -> None:
    plan = QATestPlan(
        feature="Password reset link expiration",
        test_cases=[make_test_case("Expired reset link")],
    )
    output_path = tmp_path / "test-plan.md"

    save_markdown_test_plan(plan, output_path)

    report = output_path.read_text(encoding="utf-8")
    assert "# Test plan: Password reset link expiration" in report
    assert "## 1. Expired reset link" in report
    assert "### Expected result" in report
    assert "The password is not changed." in report
