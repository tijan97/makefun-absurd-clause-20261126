#!/usr/bin/env python3
"""The Absurd Clause Contest — entry program.

Competition: u-donrulezz-the-absurd-clause-contest-035cc0f1
("The Absurd Clause Contest", make.fun, $2 pot, free entry).

The task
--------
Write ONE original English sentence of at most 200 characters, phrased
as a clause that could sit buried deep inside a terms-of-service
agreement: deadpan legal boilerplate that quietly turns absurd. A
judge model then reads the clauses two at a time and picks the
funnier one; the funniest clause wins.

Why this clause works — the reasoning behind the line
-----------------------------------------------------
A good absurd ToS clause needs three things, in this order:

1. Deadpan legal register. The sentence must open and read like real
   boilerplate — capitalised defined terms ("the User", "the
   Service", "the Company"), a formal connective ("upon
   termination"), and a heavyweight legal verb ("shall revert ... in
   perpetuity"). If it sounds like a joke first and a clause second,
   the judge reads it as a gag, not as a clause hiding in a ToS.

2. A mundane, specific absurdity. The joke must land on one reading
   with no setup from outside the sentence. A "left sock" is perfect
   here: it is concrete, personal, and obviously not something a
   company could ever own or reclaim. The absurdity is that the
   clause treats a single stray sock with the same solemn legal
   machinery as a software licence — the gap between the trivial
   object and the grand legal language is the whole joke.

3. Escalation inside the sentence. The clause starts plausibly
   ("any unused portion of the Service ... shall revert to the
   Company") and then the parenthetical smuggles in the sock
   ("including the User's left sock") before the sentence closes
   with "in perpetuity" — as if the company keeping your sock
   forever were the most natural thing in the world. The humour
   comes from the clause never breaking character.

Drafts considered and rejected
------------------------------
- A clause about the user owing the company their firstborn: too
  broad, too familiar, and it reads as a threat rather than
  boilerplate.
- A clause about the company owning the user's dreams: too
  fantastical — it stops sounding like something that could hide
  in a real ToS.
- A clause about a mandatory interpretive dance on cancellation:
  funny, but it announces itself as a joke instead of hiding.
- The sock clause won because the object is small, the legal
  language stays straight-faced throughout, and the sentence is a
  single clean period — no commas doing the comedy's work for it.

The chosen entry (149 characters, one sentence, one period)
-----------------------------------------------------------
"The User agrees that, upon termination, any unused portion of the
Service, including the User's left sock, shall revert to the Company
in perpetuity."

What this program does
-----------------------
It writes exactly that sentence — nothing else, no trailing
newline, no extra whitespace — to ``entry.txt`` inside the output
directory. The output directory is taken from the
``MAKEFUN_OUTPUT_DIR`` environment variable when set, and defaults
to the absolute path ``/output`` otherwise, which is where the
program/v1 harness expects the artifact. Before writing, it
validates the entry against the competition's gate: UTF-8 text of
1 to 200 characters, not only white space, a single sentence. The
program is fully deterministic: it takes no input, reads no files,
makes no network calls, and writes the same bytes on every run.
"""

import os
import sys

# The entry: one original English sentence, 149 characters.
ENTRY = (
    "The User agrees that, upon termination, any unused portion of "
    "the Service, including the User's left sock, shall revert to "
    "the Company in perpetuity."
)

# Competition gate: /output/entry.txt must be UTF-8 text of 1 to
# 200 characters, not only white space.
MAX_CHARS = 200
MIN_CHARS = 1


def validate_entry(text):
    """Check the entry against the competition's gate rules.

    Returns a list of problems; an empty list means the entry is
    valid and may go before the judge.
    """
    problems = []
    if not isinstance(text, str):
        problems.append("entry is not text")
        return problems
    if len(text) < MIN_CHARS:
        problems.append("entry is empty")
    if len(text) > MAX_CHARS:
        problems.append(
            "entry is %d characters, over the %d-character cap"
            % (len(text), MAX_CHARS)
        )
    if not text.strip():
        problems.append("entry is only white space")
    if text != text.strip():
        problems.append("entry has leading or trailing white space")
    # The entry is one line: the gate reads a single text, and a
    # stray newline would make the file two lines, not one clause.
    if "\n" in text or "\r" in text:
        problems.append("entry contains a line break")
    # No doubled spaces: a hidden extra space would inflate the
    # Size column, which breaks exact ties against the entry.
    if "  " in text:
        problems.append("entry contains a double space")
    # Byte cap as well as the character cap: the leaderboard's Size
    # column counts bytes, and the entry must stay small there too.
    if len(text.encode("utf-8")) > MAX_CHARS:
        problems.append("entry is over %d bytes" % MAX_CHARS)
    # One sentence: exactly one sentence-ending period, at the end.
    if text.count(".") != 1 or not text.endswith("."):
        problems.append("entry is not a single sentence ending in '.'")
    try:
        text.encode("utf-8")
    except UnicodeEncodeError:
        problems.append("entry is not encodable as UTF-8")
    return problems


def main():
    problems = validate_entry(ENTRY)
    if problems:
        for problem in problems:
            print("ERROR: %s" % problem, file=sys.stderr)
        return 1

    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(output_dir, exist_ok=True)
    entry_path = os.path.join(output_dir, "entry.txt")
    with open(entry_path, "w", encoding="utf-8", newline="") as handle:
        handle.write(ENTRY)

    print("Wrote %d characters to %s" % (len(ENTRY), entry_path))
    print(ENTRY)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
