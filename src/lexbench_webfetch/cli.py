"""Small command interface for portable benchmark inputs."""
import argparse
import json
from pathlib import Path

from .benchmark import export, inspect_annotation_revision, registry, validate, verify_inputs


def main() -> None:
    parser = argparse.ArgumentParser(description="Inspect and verify LexBench Web Fetch inputs")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("list", help="List the versioned suites")
    check = sub.add_parser("validate", help="Check all public definitions and bindings")
    check.add_argument("--suite")
    for name in ("verify-inputs", "export"):
        command = sub.add_parser(name)
        command.add_argument("--suite", required=True)
        command.add_argument("--source", type=Path, required=True)
        if name == "export":
            command.add_argument("--output", type=Path, required=True)
            command.add_argument("--revision", help="Apply a registered score-only annotation version")
    inspect = sub.add_parser("inspect-revision", help="Show reviewed field differences, sources and acceptance controls")
    inspect.add_argument("--suite", required=True)
    inspect.add_argument("--revision", required=True)
    score = sub.add_parser("score", help="Evaluate a saved response and delivered files")
    score.add_argument("--task", type=Path, required=True,
                       help="Complete task JSON including its frozen reference requirements")
    score.add_argument("--response", type=Path, required=True)
    score.add_argument("--file", type=Path, action="append", default=[])
    score.add_argument("--list-reference", type=Path)
    score.add_argument("--metadata", type=Path, help="Saved answer metadata as a JSON object")
    score.add_argument("--request-failed", action="store_true")
    score.add_argument("--status-code", type=int)
    score.add_argument("--final-url")
    score.add_argument("--title")
    compile_rules = sub.add_parser("compile-access-restrictions")
    compile_rules.add_argument("--output", type=Path, required=True)
    compile_rules.add_argument("--definition-dir", type=Path)
    compile_rules.add_argument("--evidence-home", type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.command == "inspect-revision":
            result = inspect_annotation_revision(args.suite, args.revision)
        elif args.command == "score":
            from .evaluation import evaluate_response
            metadata = json.loads(args.metadata.read_text(encoding="utf-8")) if args.metadata else None
            if args.metadata and not isinstance(metadata, dict):
                raise ValueError("Answer metadata must be a JSON object")
            result = evaluate_response(
                json.loads(args.task.read_text(encoding="utf-8")), args.response.read_bytes(),
                files=[path.read_bytes() for path in args.file], ok=not args.request_failed,
                metadata=metadata,
                list_reference=(json.loads(args.list_reference.read_text(encoding="utf-8"))
                                if args.list_reference else None), status_code=args.status_code,
                title=args.title, final_url=args.final_url)
        elif args.command == "compile-access-restrictions":
            from .risk_control_dataset import build, RISK
            result = build(args.output, args.definition_dir or RISK, evidence_home=args.evidence_home)
        elif args.command == "list":
            result = [{k: row[k] for k in ("id", "dataset_id", "case_count")} for row in registry()["suites"]]
        elif args.command == "validate":
            result = [validate(row["id"]) for row in registry()["suites"]
                      if args.suite is None or row["id"] == args.suite]
            if not result:
                raise ValueError(f"Unknown suite: {args.suite}")
        elif args.command == "verify-inputs":
            result = verify_inputs(args.suite, args.source)
        else:
            result = {"dataset": str(export(args.suite, args.source, args.output, revision=args.revision).resolve())}
    except (ValueError, KeyError, OSError) as error:
        parser.exit(1, f"{error}\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
