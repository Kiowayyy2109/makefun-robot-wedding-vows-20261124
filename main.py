"""One-Line Robot Wedding Vows — make.fun entry.

Writes one line (at most 160 characters) to /output/entry.txt: a robot's
wedding vow. The joke is a captcha twist only a robot could make: the vow
opens in the classic wedding form and pays off in the last few words.
"""

import os
from pathlib import Path

# The chosen entry text (131 Unicode code points). Classic vow frame
# ("I take you to be my lawfully wedded wife") plus an explicit promise,
# then the turn: a robot solemnly promising to click "I am not a robot".
ENTRY = (
    "I take you to be my lawfully wedded wife, and I promise to always "
    "click 'I am not a robot' for you \u2014 even though we both know I am."
)

# Length guard: the gate requires 1-160 Unicode code points, not whitespace only.
length = len(list(ENTRY))
if length < 1 or length > 160:
    raise SystemExit(f"entry length {length} code points is outside 1-160")
if not ENTRY.strip():
    raise SystemExit("entry must not be only whitespace")
if ENTRY != ENTRY.strip():
    raise SystemExit("entry must not have leading or trailing whitespace")
if "\n" in ENTRY or "\r" in ENTRY:
    raise SystemExit("entry must be a single line")

# Output dir per the kit contract: $MAKEFUN_OUTPUT_DIR, else /output/entry.txt.
out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
out_dir.mkdir(parents=True, exist_ok=True)
entry_path = out_dir / "entry.txt"
entry_path.write_bytes(ENTRY.encode("utf-8"))

# Also write to /output/entry.txt when the env dir differs, so either
# location the grader reads holds the same bytes.
if out_dir != Path("/output"):
    try:
        Path("/output").mkdir(parents=True, exist_ok=True)
        Path("/output/entry.txt").write_bytes(ENTRY.encode("utf-8"))
    except OSError:
        # The env-dir copy above is the contract; this one is best-effort.
        pass

# Verify the write round-trips byte-for-byte before reporting success.
if entry_path.read_bytes() != ENTRY.encode("utf-8"):
    raise SystemExit("entry.txt does not match the entry text after writing")

# Re-read as text and confirm it is still exactly one line.
if entry_path.read_text(encoding="utf-8").count("\n") != 0:
    raise SystemExit("entry.txt must be a single line")

print(f"wrote entry.txt ({length} code points)")
