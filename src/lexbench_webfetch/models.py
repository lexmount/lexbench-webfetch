from __future__ import annotations
import re
from dataclasses import dataclass, field
from typing import Any

from .paths import safe_identifier, validate_http_url

TASK_KINDS = ('body', 'structure', 'resource', 'file')


TRACKS = {
    'web': '普通网页正文', 'dynamic': '动态网站正文', 'challenge': '热门网站正文',
    'risk_control': '风控网页正文',
    'document': '文档正文', 'image': '图片获取', 'video': '视频获取',
}


_IMPLEMENTATION_INSTRUCTION_PATTERNS = (
    re.compile(r"(?:不要求|不需要|不要|不得|禁止|不)(?:点击|输入|滚动|翻页|登录|搜索|使用OCR)"),
    re.compile(r"Browser Use 操作", re.IGNORECASE),
    re.compile(r"(?:允许(?:渲染|解析|加载子文档|获取公开接口)|不限制实现路径)"),
    re.compile(r"(?:匿名|已登录|登录态)(?:的|状态下的)?(?:浏览器|会话|访问)"),
    re.compile(
        r"\b(?:do not|don't|must not|without)\s+"
        r"(?:click(?:ing)?|typ(?:e|ing)|scroll(?:ing)?|paginat(?:e|ing)|"
        r"log(?:ging)?\s+in|sign(?:ing)?\s+in|search(?:ing)?|use\s+(?:a\s+)?browser)",
        re.IGNORECASE,
    ),
    re.compile(r"\b(?:anonymous|authenticated)\s+(?:browser|session)\b", re.IGNORECASE),
)


def validate_outcome_contract(
    case_id: str,
    task_prompt: str,
    reference_answer: str = "",
    description: str = "",
) -> None:
    """Reject task answers that prescribe a participant's retrieval implementation."""
    for field_name, value in (
        ("task_prompt", task_prompt),
        ("reference_answer", reference_answer),
        ("description", description),
    ):
        if not isinstance(value, str):
            raise ValueError(f"{field_name} must be text: {case_id}")
        if any(pattern.search(value) for pattern in _IMPLEMENTATION_INSTRUCTION_PATTERNS):
            raise ValueError(
                f"{field_name} must define the requested outcome, not retrieval actions: {case_id}"
            )


@dataclass(frozen=True)
class EvalCase:
    id: str
    name: str
    url: str
    category: str
    expected_any: list[str]
    description: str = ""
    tags: list[str] = field(default_factory=list)
    required_facts: list[dict[str, Any]] = field(default_factory=list)
    forbidden_any: list[str] = field(default_factory=list)
    min_content_chars: int = 1
    fact_coverage_threshold: float = 1.0
    ground_truth_evidence: list[dict[str, str]] = field(default_factory=list)
    task_prompt: str = ""
    reference_answer: str = ""
    source_benchmark: dict[str, Any] = field(default_factory=dict)
    ground_truth_main_content: str = ""
    expected_resources: list[dict[str, Any]] = field(default_factory=list)
    resource_output_contract: dict[str, Any] = field(default_factory=dict)
    content_score_applicable: bool = True
    track: str = "web"
    required_patterns: list[dict[str, Any]] = field(default_factory=list)
    source_verification: dict[str, Any] = field(default_factory=dict)
    task_kind: str = "body"
    acceptance_contract: dict[str, Any] = field(default_factory=dict)
    composite_acceptance: dict[str, Any] = field(default_factory=dict)
    mutable_body_policy: dict[str, Any] = field(default_factory=dict)
    body_requirements: dict[str, Any] = field(default_factory=dict)
    retrieval_hints: dict[str, Any] = field(default_factory=dict)
    source_review_url: str = ""
    evaluation_url: str = ""
    expected_final_url: str = ""
    expected_document_language: str = ""
    expected_document_language_present: bool = True
    target_language: str = ""
    target_region: str = ""
    rule_review: dict[str, Any] = field(default_factory=dict)


def validate_case(case: EvalCase) -> None:
    """Validate required fields, routing and identity before acquisition."""
    safe_identifier(case.id)
    validate_http_url(case.url)
    if not isinstance(case.name, str) or not case.name.strip():
        raise ValueError(f"Task name must be nonempty text: {case.id}")
    if not isinstance(case.category, str):
        raise ValueError(f"Task category must be text: {case.id}")
    validate_outcome_contract(
        case.id, case.task_prompt, case.reference_answer, case.description
    )
    if not isinstance(case.expected_any, list) or any(
        not isinstance(marker, str) or not marker.strip() for marker in case.expected_any
    ):
        raise ValueError(f"expected_any must be a list of nonempty text markers: {case.id}")
    if case.task_kind not in TASK_KINDS:
        raise ValueError(f"Unknown task kind for {case.id}: {case.task_kind}")
    if not isinstance(case.track, str) or case.track not in TRACKS:
        raise ValueError(f"Unknown task track for {case.id}: {case.track}")

