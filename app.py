import argparse
import os

from dotenv import load_dotenv

from generator import (
    generate_test_plan,
    load_test_plan,
    save_markdown_test_plan,
    save_test_plan,
)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate structured QA scenarios from a feature description."
    )
    parser.add_argument(
        "--feature",
        help="Feature description. If omitted, the program asks for it interactively.",
    )
    parser.add_argument(
        "--input-json",
        help=(
            "Validate and format an AI-generated JSON test plan without "
            "making an API call."
        ),
    )
    parser.add_argument(
        "--output",
        default="generated_test_plan.json",
        help="Path of the JSON file to create.",
    )
    parser.add_argument(
        "--markdown-output",
        default="generated_test_plan.md",
        help="Path of the human-readable Markdown report to create.",
    )
    return parser.parse_args()


def main() -> None:
    load_dotenv()
    args = parse_arguments()

    if not args.input_json and not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY is missing. Add it to a local .env file.")
        raise SystemExit(1)

    try:
        if args.input_json:
            test_plan = load_test_plan(args.input_json)
        else:
            feature_description = args.feature or input(
                "Describe the feature you want to test:\n> "
            )
            test_plan = generate_test_plan(feature_description)
        output_path = save_test_plan(test_plan, args.output)
        markdown_path = save_markdown_test_plan(
            test_plan, args.markdown_output
        )
    except (ValueError, RuntimeError) as error:
        print(f"Could not generate the test plan: {error}")
        raise SystemExit(1) from error
    except Exception as error:
        print(f"The API request failed: {error}")
        raise SystemExit(1) from error

    print(f"\nGenerated {len(test_plan.test_cases)} test cases:\n")
    for number, test_case in enumerate(test_plan.test_cases, start=1):
        print(
            f"{number}. [{test_case.priority.upper()}] "
            f"{test_case.title} ({test_case.category})"
        )

    print(f"\nJSON test plan saved to {output_path}")
    print(f"Readable report saved to {markdown_path}")


if __name__ == "__main__":
    main()
