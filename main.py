"""Best Advice I Ever Got — one sentence, written to /output/entry.txt.

The whole entry is a single sentence of advice, at most 200 characters.
This program stores that sentence, checks it against the competition gate
(UTF-8 text, 1 to 200 characters, not only white space), and writes it out
atomically so a grader never reads a half-written file.
"""

import os
import sys

SENTENCE = (
    "My mother said, 'If you have to talk yourself into it, the answer is "
    "no,' and every bad decision I own began with me talking."
)

OUTPUT_DIR = "/output"
OUTPUT_NAME = "entry.txt"
MAX_CHARS = 200


def validate(text):
    """Return the text unchanged if it passes the gate, else raise."""
    if not isinstance(text, str):
        raise TypeError("entry must be text")
    if text.strip() == "":
        raise ValueError("entry is only white space")
    if len(text) < 1 or len(text) > MAX_CHARS:
        raise ValueError("entry must be 1 to %d characters" % MAX_CHARS)
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    text.encode("utf-8")  # raises if the text is not encodable
    return text


def write_entry(text, out_dir=OUTPUT_DIR):
    """Write text to <out_dir>/entry.txt via a staging file, then verify."""
    os.makedirs(out_dir, exist_ok=True)
    final_path = os.path.join(out_dir, OUTPUT_NAME)
    staging_path = final_path + ".staging"
    with open(staging_path, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(staging_path, final_path)
    with open(final_path, "r", encoding="utf-8") as handle:
        written = handle.read()
    if written != text:
        raise IOError("read-back mismatch: %r != %r" % (written, text))
    return final_path


def main():
    sentence = validate(SENTENCE)
    path = write_entry(sentence)
    print("wrote %d chars to %s" % (len(sentence), path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
