# Split a full file into the header section and the rest. Mainly just QOL for
# the other functions, so they can do stuff based on only one of these without
# manually splitting. This will probably break on some hunks, but this whole
# file is just temporary for me to figure out logic before upstreaming to
# splitpatch
def splitHeader(rawFile):
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

    return (header, contents)


# Take a line like `@@ -18,9 +20,11 @@` and extract the relevant values
def extractHunkValues(hunk_line):
    hunk_line = hunk_line[3:-3]  # Take off the @@ stuff
    halves = hunk_line.split(" ")  # ["-18,9", "+20,11"]
    if len(halves) != 2:
        print("Uh oh... there were more spaces than I thought possible")

    old_values = halves[0].split(",")  # ["-18", "9"]
    new_values = halves[1].split(",")  # ["+20", "11"]

    old_start = int(old_values[0].strip("-"))  # 18
    old_len = int(old_values[1])  # 9

    new_start = int(new_values[0].strip("+"))  # 20
    new_len = int(new_values[1])  # 11

    # Tuples are inherently arbitary, but we return in the order seen in the
    # actual string.
    return (old_start, old_len, new_start, new_len)


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
    print(f"added lines: {added_lines}")
    print(f"deleted lines: {deleted_lines}")
    print(f"unchanged lines: {unchanged_lines}")

    # To reach the old length, just bring back deleted lines
    oldLength = unchanged_lines + deleted_lines

    # To reach the new length, take what wasn't changed, and add new stuff
    # Yes, these comments seem obvious. But it took a moment for me to
    # realize this was how things worked!
    newLength = unchanged_lines + added_lines

    return (oldLength, newLength)
