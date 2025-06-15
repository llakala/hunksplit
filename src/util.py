import re


# Returns the line at which the
def is_valid_hunk(text: str) -> bool:
    lines = text.splitlines()
    for line in lines:
        # If any of the lines start a hunk, this is valid!
        if re.search("^@@", line) is not None:
            return True

    return False


# Split a full file into the header section and the rest. Mainly just QOL for
# the other functions, so they can do stuff based on only one of these without
# manually splitting. This will throw an exception if the header never ends,
# and this patch is actually one with only metadata (like "Deleted file"). You
# should filter that kind of file out before this!
def split_header(rawFile: str) -> tuple[list[str], list[str]]:
    header = []
    contents = []
    lines = rawFile.splitlines()
    in_header = True

    for line in lines:
        if in_header:
            header.append(line)
        else:
            contents.append(line)

        if line.startswith("@@ "):
            in_header = False

    if contents == []:
        raise Exception("The header never ended!")

    return (header, contents)


# Based on the contents, find the old/new lengths of the hunk,
# for use in the header.
def lengths(contents):
    added_lines = 0
    deleted_lines = 0
    unchanged_lines = 0

    for line in contents:
        # Debug
        # print(f"Line {i}: {line}")
        match line[0]:
            case "+":
                added_lines += 1
            case "-":
                deleted_lines += 1
            case " ":
                unchanged_lines += 1
            case _:
                print("Well, this is crazy. ERROR! ERROR!")

    # DEBUG
    # print(f"added lines: {added_lines}")
    # print(f"deleted lines: {deleted_lines}")
    # print(f"unchanged lines: {unchanged_lines}")

    # To reach the old length, just bring back deleted lines
    oldLength = unchanged_lines + deleted_lines

    # To reach the new length, take what wasn't changed, and add new stuff
    # Yes, these comments seem obvious. But it took a moment for me to
    # realize this was how things worked!
    newLength = unchanged_lines + added_lines

    return (oldLength, newLength)
