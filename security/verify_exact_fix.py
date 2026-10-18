#!/usr/bin/env python3
import subprocess
from pathlib import Path
BASE = "e3de715222b2667c54a267441159a5729f11155e"
FILE = "common/chat-peg-parser.cpp"
old = subprocess.check_output(["git", "show", f"{BASE}:{FILE}"])
new = Path(FILE).read_bytes()
needle = b"            pending_tool_call.reset();\n        }\n    }\n}\n\ncommon_peg_parser common_chat_peg_builder::standard_constructed_tools("
assert old.count(needle) == 1, "Unexpected baseline parser"
expected = old.replace(needle, needle.replace(b"            pending_tool_call.reset();\n", b"            pending_tool_call.reset();\n            current_tool = nullptr;\n", 1), 1)
assert new.replace(b"\r\n", b"\n") == expected.replace(b"\r\n", b"\n"), "Production patch not exactly upstream one-line fix"
changed = set(subprocess.check_output(["git", "diff", "--name-only", BASE, "HEAD"], text=True).splitlines())
approved = {FILE, "security/verify_exact_fix.py", ".github/workflows/prismml-security-cuda13.yml"}
assert changed == approved, f"Unexpected or missing changes: {changed ^ approved}"
subprocess.run(["git", "diff", "--check", BASE, "HEAD"], check=True)
print("PASS: exactly upstream patch; no other production changes")
