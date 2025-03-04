import hunk

filename = "test.patch"
with open(filename, "r") as f:
    contents = f.read()


header, contents = hunk.splitHeader(contents)

# splitHeader returns a list, because that's easiest for it.
# you can turn it to a string manually for printing
joined_header = "\n".join(header)
joined_contents = "\n".join(contents)

# The length of the hunk, prefixed with `gen` because these were generated
# from the file contents
gen_old_len, gen_new_len = hunk.lengths(contents)
print(f"Generated old len: {gen_old_len}")
print(f"Generated new len: {gen_new_len}")

# Example - ideally this would be found from the header automatically
hunkLine = "@@ -18,9 +18,11 @@"

old_start, old_len, new_start, new_len = hunk.extractHunkValues(hunkLine)

print(f"Old len: {old_len}")
print(f"New len: {new_len}")

print(f"Old start: {old_start}")
print(f"New start: {new_start}")
