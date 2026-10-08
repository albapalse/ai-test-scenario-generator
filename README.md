# AI Test Scenario Generator

A small Python tool that converts a feature description into a structured QA
test plan with the help of a large language model.

The project was created as a practical experiment in AI-assisted QA. It focuses
on a narrow task: producing an initial checklist that a human tester can review,
edit, and extend.

## What it does

- Generates happy-path, negative, edge-case, and accessibility scenarios.
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
│   └── password_reset.txt
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

### Free workflow without API credit

An AI assistant can generate JSON that follows the structures in `models.py`.
The application can then validate, deduplicate, and format that response without
making a paid API call:

```bash
python app.py --input-json examples/password_reset_plan.json
```

This example plan was generated with Codex and then reviewed as part of the
project. The program rejects malformed responses instead of trusting AI output
automatically.

## Tests

The automated tests do not call the AI API or consume API credit:

```bash
pytest
```

They verify input validation, AI-response import, rejection of malformed
responses, duplicate removal, and JSON and Markdown export.

## How I used AI

I used Codex as an AI coding assistant to discuss the scope, create an initial
implementation, and identify useful validation and error-handling cases. I
reviewed the project structure, ran the tests, and used the resulting project
to understand how structured model output can support a QA workflow. I chose to
add a Markdown report because raw JSON is useful for automation but inconvenient
for a tester who needs to review and discuss the generated scenarios.

The application also uses an LLM to generate the initial test scenarios. The
model output is treated as a starting point, not as a finished test plan.
When API credit is unavailable, the same review pipeline can process a response
generated interactively with an AI assistant.

## Limitations

- The quality of the scenarios depends on the detail in the feature description.
- The model does not know undocumented business rules or product history.
- A valid structure does not guarantee that every scenario is useful or correct.
- A human tester still needs to review priorities, assumptions, and coverage.

## Possible next steps

- Add product-specific context to the prompt.
- Generate Playwright test templates for selected scenarios.
- Compare generated scenarios against a manually written reference set.
