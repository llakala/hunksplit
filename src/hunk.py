import re


class Hunk:
    old_start = None
    old_len = None

    new_start = None
    new_len = None

    header = []
    contents = []

    # Given a hunk's header and its contents, create a Hunk object.
    def __init__(self, header: list[str], contents: list[str]):
        # TODO: differentiate between junk header and real header?
        self.header = header
        self.contents = contents

        # The header has multiple lines, but only the last one will give us the
        # info we need
        header_line = header[-1]

        regex = re.match(r"^@@ -(\d+),(\d+) \+(\d+),(\d+) @@", header_line)

        if regex is None:
            raise Exception("Failed to parse header line!")

        self.old_start = regex.group(1)
        self.old_len = regex.group(2)
        self.new_start = regex.group(3)
        self.new_len = regex.group(4)

    def can_be_split(self) -> bool:
        started = False
        ended = False

        for line in self.contents:
            kind = line[0]
            is_change = kind == "+" or kind == "-"

            # We started with some + or - lines, constituting something that
            # could be a hunk. Then, we had a break, with some unchanged lines.
            # And, now, we see another change! This hunk can be split.
            if started and ended and is_change:
                return True

            # We're currently in a section, and just got to an unchanged line,
            # so the section is over!
            elif started and kind == " ":
                ended = True

            # We haven't started a section yet, but we just saw a line change!
            # The section begins.
            elif not started and is_change:
                started = True

        return False

    def __str__(self):
        return (
            f"start: L{self.old_start} -> L{self.new_start}\n"
            + f"len: {self.old_len} -> {self.new_len}"
        )
