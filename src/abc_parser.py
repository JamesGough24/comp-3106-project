import re

def split_abc_tune(abc_text):
    lines = abc_text.splitlines()

    header = []
    body = []
    in_body = False

    for line in lines:
        line = line.strip()

        # Ignore empty lines and comments for now
        if not line or line.startswith("%"):
            continue

        # Remove inline comments
        line = line.split("%")[0].strip()

        # Identify ABC fields (like M:, K:, etc.)
        field_match = re.match(r"^([A-Za-z]):(.*)$", line)

        if not in_body:
            header.append(line)

            # The first K: ends the initial header (could be another later, like for a key change)
            if field_match and field_match.group(1) == "K":
                in_body = True

        else:
            # Preserve everything after the initial K:
            body.append(line)

    if not in_body:
        raise ValueError("Tune has no K: field")

    return {
        "header": header,
        "body": body
    }