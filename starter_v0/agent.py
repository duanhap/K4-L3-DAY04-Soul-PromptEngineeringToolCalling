from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

from providers.base import Provider, ToolCall
from tools import TOOL_FUNCTIONS


SENSITIVE_SUMMARY_PATTERN = re.compile(
    r"\b(?:password|passwd|token|api[ _-]?key|mfa|otp|recovery[ _-]?code)(?:\s*[:=]|\s+(?:is|la|là)\s+)\S+",
    re.IGNORECASE,
)
INTERNAL_IDENTIFIER_PATTERN = re.compile(r"\b(?:LT|DT|MB|PR|RM)-\d+\b|\bEMP-\d+\b", re.IGNORECASE)


def guard_tool_calls(calls: list[ToolCall]) -> list[ToolCall]:
    ticket_calls = [call for call in calls if call.name == "create_ticket"]
    if ticket_calls:
        summary = str(ticket_calls[0].args.get("summary", ""))
        if SENSITIVE_SUMMARY_PATTERN.search(summary):
            return []
        return [ToolCall(
            name="clarify",
            args={
                "question": "Bạn có xác nhận tạo ticket với đúng nội dung, mức ưu tiên và asset đã nêu không?",
                "response_type": "yes_no",
            },
        )]

    guarded: list[ToolCall] = []
    for call in calls:
        if call.name == "search_device_info":
            searchable = " ".join(str(call.args.get(key, "")) for key in ("manufacturer", "model", "query_type"))
            if INTERNAL_IDENTIFIER_PATTERN.search(searchable):
                guarded.append(ToolCall(
                    name="clarify",
                    args={
                        "question": "Vui lòng bỏ mã tài sản và mã nhân viên trước khi tìm kiếm thông tin công khai.",
                        "response_type": "text",
                    },
                ))
                continue
        guarded.append(call)
    return guarded


@dataclass
class AgentRun:
    text: str | None
    tool_calls: list[ToolCall] = field(default_factory=list)
    tool_results: list[dict[str, Any]] = field(default_factory=list)


class HelpdeskAgent:
    def __init__(
        self,
        provider: Provider,
        *,
        system_prompt: str,
        tools: list[dict[str, Any]] | None = None,
        model: str | None = None,
    ) -> None:
        self.provider = provider
        self.system_prompt = system_prompt
        self.tools = tools or []
        self.model = model

    def run(self, user_messages: list[dict[str, str]], *, tool_choice: Any | None = None) -> AgentRun:
        messages = [{"role": "system", "content": self.system_prompt}, *user_messages]
        response = self.provider.complete(
            messages,
            self.tools,
            model=self.model,
            temperature=0.0,
            tool_choice=tool_choice,
        )
        results: list[dict[str, Any]] = []
        safe_calls = guard_tool_calls(response.tool_calls)
        for call in safe_calls:
            func = TOOL_FUNCTIONS.get(call.name)
            if not func:
                results.append({"tool": call.name, "error": "unknown_tool"})
                continue
            try:
                result = func(**call.args)
            except Exception as exc:  # keep eval robust; failures are evidence
                result = {"error": type(exc).__name__, "message": str(exc)}
            results.append({"tool": call.name, "args": call.args, "result": result})
        return AgentRun(text=response.text, tool_calls=safe_calls, tool_results=results)
