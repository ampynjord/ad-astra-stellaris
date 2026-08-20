# -*- coding: utf-8 -*-
"""Petit parseur Clausewitz partage par les outils Ad Astra."""
import re


def top_level_blocks(text):
    """Rend (cle, debut, fin) pour chaque bloc `cle = { ... }` de niveau 0.
    Ignore les accolades situees dans un commentaire."""
    out, i, n = [], 0, len(text)
    pat = re.compile(r"^([A-Za-z_][\w.]*)\s*=\s*\{", re.M)
    while i < n:
        match = pat.search(text, i)
        if not match:
            break
        depth, j, in_comment = 0, match.end() - 1, False
        while j < n:
            char = text[j]
            if char == "#":
                in_comment = True
            elif char == "\n":
                in_comment = False
            elif not in_comment:
                if char == "{":
                    depth += 1
                elif char == "}":
                    depth -= 1
                    if depth == 0:
                        j += 1
                        break
            j += 1
        out.append((match.group(1), match.start(), j))
        i = j
    return out


def strip_comments(text):
    return "\n".join(line.split("#", 1)[0] for line in text.splitlines())


def braces_delta(text):
    body = strip_comments(text)
    return body.count("{") - body.count("}")
