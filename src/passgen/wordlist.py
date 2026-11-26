from pathlib import Path


def unique(items):
    seen = set()
    for item in items:
        if item not in seen:
            seen.add(item)
            yield item


def write_wordlist(gen, path, *, dedupe=False):
    items = unique(gen) if dedupe else gen
    count = 0
    with Path(path).open("w", encoding="utf-8") as f:
        for word in items:
            f.write(word + "\n")
            count += 1
    return count
