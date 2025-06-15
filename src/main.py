import os

import hunk
import util


def split_hunk(filename):
    with open(filename, "r") as f:
        contents = f.read()

    # Exit early if the hunk is invalid
    if not util.is_valid_hunk(contents):
        print("This doesn't contain an actual hunk, it's weird!")
        return None

    header_lines, contents = util.split_header(contents)

    hnk = hunk.Hunk(header_lines, contents)

    if not hnk.can_be_split():
        print("Hunk doesn't need to be split")
        return None

    print(hnk)

    # The length of the hunk, prefixed with `gen` because these were generated
    # from the file contents
    # gen_old_len, gen_new_len = util.lengths(contents)
    # print(f"Generated old len: {gen_old_len}")
    # print(f"Generated new len: {gen_new_len}")


if __name__ == "__main__":
    files = os.listdir("./patches")

    for filename in files:
        print(f"Parsing {filename}")
        filename = "./patches/" + filename

        split_hunk(filename)
        print()
