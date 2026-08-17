# -*- coding: utf-8 -*-
"""Petit parseur Clausewitz partage par les outils Ad Astra."""
import re


def top_level_blocks(text):
    """Rend (cle, debut, fin) pour chaque bloc `cle = { ... }` de niveau 0.
    Ignore les accolades situees dans un commentaire."""
    out, i, n = [], 0, len(text)
    pat = re.compile(r"^([A-Za-z_][\w.]*)\s*=\s*\{", re.M)
    while i < n:
        m = pat.search(text, i)
        if not m:
            break
        depth, j, in_comment = 0, m.end() - 1, False
        while j < n:
            c = text[j]
            if c == "#":
                in_comment = True
            elif c == "\n":
                in_comment = False
            elif not in_comment:
                if c == "{":
                    depth += 1
                elif c == "}":
                    depth -= 1
                    if depth == 0:
                        j += 1
                        break
            j += 1
        out.append((m.group(1), m.start(), j))
        i = j
    return out


def strip_comments(text):
    return "\n".join(line.split("#", 1)[0] for line in text.splitlines())


def braces_delta(text):
    body = strip_comments(text)
    return body.count("{") - body.count("}")
