from __future__ import annotations

import json
import os
from pathlib import Path

from openai import OpenAI

from models import TestCase, TestPlan


SYSTEM_PROMPT = """You assist a junior QA tester.

Create a concise and practical test plan for the feature described by the user.
Include happy-path, negative, edge-case, and accessibility scenarios when relevant.
Do not invent product requirements that are not supported by the description.
Keep every step specific enough for another tester to follow.
"""


def validate_feature_description(feature_description: str) -> str:
    cleaned_description = feature_description.strip()
    if len(cleaned_description) < 20:
        raise ValueError(
            "The feature description must contain at least 20 characters."
        )
    return cleaned_description


def remove_duplicate_test_cases(test_plan: TestPlan) -> TestPlan:
    unique_cases: list[TestCase] = []
    titles_seen: set[str] = set()

    for test_case in test_plan.test_cases:
        normalized_title = " ".join(test_case.title.lower().split())
        if normalized_title not in titles_seen:
            titles_seen.add(normalized_title)
            unique_cases.append(test_case)

    return test_plan.model_copy(update={"test_cases": unique_cases})


def generate_test_plan(
    feature_description: str,
    client: OpenAI | None = None,
    model: str | None = None,
) -> TestPlan:
    feature_description = validate_feature_description(feature_description)
    api_client = client or OpenAI()
    selected_model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    completion = api_client.chat.completions.parse(
        model=selected_model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": (
                    "Create a test plan for this feature:\n\n"
                    f"{feature_description}"
                ),
            },
        ],
        response_format=TestPlan,
    )

    message = completion.choices[0].message
    if message.refusal:
        raise RuntimeError(f"The model refused the request: {message.refusal}")
    if message.parsed is None:
        raise RuntimeError("The model did not return a valid test plan.")

    return remove_duplicate_test_cases(message.parsed)


def save_test_plan(
    test_plan: TestPlan,
    output_path: str | Path = "generated_test_plan.json",
) -> Path:
    destination = Path(output_path)
    destination.write_text(
        json.dumps(test_plan.model_dump(), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return destination


def save_markdown_test_plan(
    test_plan: TestPlan,
    output_path: str | Path = "generated_test_plan.md",
) -> Path:
    destination = Path(output_path)
    lines = [f"# Test plan: {test_plan.feature}", ""]

    for number, test_case in enumerate(test_plan.test_cases, start=1):
        lines.extend(
            [
                f"## {number}. {test_case.title}",
                "",
                f"- **Category:** {test_case.category}",
                f"- **Priority:** {test_case.priority}",
                "",
                "### Preconditions",
                "",
            ]
        )
        lines.extend(f"- {item}" for item in test_case.preconditions)
        if not test_case.preconditions:
            lines.append("- None")

        lines.extend(["", "### Steps", ""])
        lines.extend(
            f"{step_number}. {step}"
            for step_number, step in enumerate(test_case.steps, start=1)
        )
        lines.extend(
            [
                "",
                "### Expected result",
                "",
                test_case.expected_result,
                "",
            ]
        )

    destination.write_text("\n".join(lines), encoding="utf-8")
    return destination
