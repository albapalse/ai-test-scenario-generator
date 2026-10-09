# AI Test Scenario Generator

A small Python tool that validates and formats AI-generated QA test plans. It
can also generate a plan directly from a feature description when API access is
configured.

The project was created as a practical experiment in AI-assisted QA. It focuses
on a narrow task: producing an initial checklist that a human tester can review,
edit, and extend.

## What it does

- Processes AI-generated happy-path, negative, edge-case, and accessibility scenarios.
- Gives every scenario a priority, preconditions, steps, and an expected result.
- Uses a typed Pydantic schema to validate the model response.
- Removes scenarios with duplicate titles.
- Exports the reviewed structure to JSON and readable Markdown.
- Handles missing configuration, invalid input, refusals, and API failures.

## Project structure

```text
.
├── app.py
├── generator.py
├── models.py
├── examples/
│   ├── password_reset.txt
│   ├── password_reset_plan.json
│   └── password_reset_report.md
└── tests/
    └── test_generator.py
```

## Setup

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Copy the example configuration and add your own API key:

```bash
cp .env.example .env
```

The local `.env` file is ignored by Git and must never be committed.
An API key is optional when using the free import workflow described below.

## Usage

### Optional API workflow

With an API key configured, the tool can request a test plan directly from a
model. This integration is optional and was not used for the included demo.

Interactive mode:

```bash
python app.py
```

Or pass a feature directly:

```bash
python app.py --feature "A reset link expires after 30 minutes and can only be used once."
```

The generated plan is saved as `generated_test_plan.json` for machines and
`generated_test_plan.md` for human review.

### Free workflow used for the demo

An AI assistant can generate JSON that follows the structures in `models.py`.
The application can then validate, deduplicate, and format that response without
making a paid API call:

```bash
python app.py --input-json examples/password_reset_plan.json
```

The included example plan was generated with Codex and then reviewed. The
program rejects malformed responses instead of trusting AI output
automatically. Its purpose is to automate the preparation and formatting of a
test plan; it does not execute tests against a real website or mobile app.

You can view the resulting report without running the project:

- [`examples/password_reset_report.md`](examples/password_reset_report.md)

## Tests

The automated tests do not call the AI API or consume API credit:

```bash
pytest
```

They verify input validation, AI-response import, rejection of malformed
responses, duplicate removal, and JSON and Markdown export.

## How I used AI

I started with a simple question: could AI create a useful QA checklist without
being trusted blindly? I used Codex to help me build the first version, and then
added checks for invalid responses and duplicate test cases. I also added
Markdown export because reviewing the raw JSON was inconvenient.

The generated scenarios still need human review, especially when the original
feature description does not include all the product rules. For the included
demo, Codex generated the initial JSON and the application validated and
formatted it without making a paid API call.

## Limitations

- The quality of the scenarios depends on the detail in the feature description.
- The model does not know undocumented business rules or product history.
- A valid structure does not guarantee that every scenario is useful or correct.
- A human tester still needs to review priorities, assumptions, and coverage.
- The current project prepares test scenarios but does not run UI tests.

## Possible next steps

- Add product-specific context to the prompt.
- Generate Playwright test templates for selected scenarios.
- Compare generated scenarios against a manually written reference set.
