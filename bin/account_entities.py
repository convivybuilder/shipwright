#!/usr/bin/env python3
"""Which entities an install's record names, and the account pairs each gets.

Read in one place and reused by `provision-accounts`, `install-privileged`,
`uninstall-builder` and `stand-up-backend`, so they cannot disagree about
where the entities list comes from, what makes a name valid, or what an
entity's accounts are called.

`read_entities` applies the exact rule `payload/skills/new-crew/SKILL.md`
documents under "Register the crew in the projects registry": a missing file
or a missing `entities` key means a single entity named `default`; anything
else that is not a non-empty list of distinct lower-case names is refused,
naming the file.
"""

from __future__ import annotations

import json
import re

DEFAULT_INSTALL_JSON = "/opt/builder/install.json"
ENTITY_NAME = re.compile(r"[a-z][a-z0-9-]*")


class EntitiesInvalid(Exception):
    """The install's record has no readable, valid entities list."""


def read_entities(path: str = DEFAULT_INSTALL_JSON) -> list[str]:
    """The install's entities, read from `path` (the install's own record).

    A missing file, or one whose object has no `entities` key, means a
    single entity named `default`. Anything else that is not a non-empty
    list of distinct lower-case names (`[a-z][a-z0-9-]*`) raises
    `EntitiesInvalid`, naming `path`.
    """
    try:
        doc = json.load(open(path, encoding="utf-8"))
    except FileNotFoundError:
        doc = {}
    except (OSError, ValueError) as exc:
        raise EntitiesInvalid(f"{path} cannot be read: {exc}") from exc
    if not isinstance(doc, dict):
        raise EntitiesInvalid(f"{path} does not hold a JSON object")
    entities = doc.get("entities", ["default"])
    if not (isinstance(entities, list) and entities
            and all(isinstance(e, str) and ENTITY_NAME.fullmatch(e) for e in entities)
            and len(set(entities)) == len(entities)):
        raise EntitiesInvalid(f"{path} lists entities as {entities!r}, not as distinct lower-case names")
    return entities


def account_pairs(entities: list[str]) -> list[tuple[str, str]]:
    """One (agents, reviewers) account-name pair per entity.

    With a single entity, whatever its name, the pair is the bare `agents`
    and `reviewers` names every install used before entities existed. With
    more than one, each entity's pair is `<entity>-agents`/`<entity>-reviewers`.
    """
    if len(entities) == 1:
        return [("agents", "reviewers")]
    return [(f"{entity}-agents", f"{entity}-reviewers") for entity in entities]


def render_sudoers(template: str, agents_names: list[str], launcher: str) -> str:
    """The sudoers template rendered once per agents account.

    The template's comment lines (and blank lines) are its header and are
    kept once; its remaining lines are the repeatable `Defaults`/rule block,
    rendered once per name in `agents_names` with `@ACCOUNT@` replaced by
    that name, then `@LAUNCHER@` replaced by `launcher` across the whole
    result.
    """
    lines = template.splitlines(keepends=True)
    header = "".join(line for line in lines if not line.strip() or line.lstrip().startswith("#"))
    block = "".join(line for line in lines if line.strip() and not line.lstrip().startswith("#"))
    body = "".join(block.replace("@ACCOUNT@", name) for name in agents_names)
    return (header + body).replace("@LAUNCHER@", launcher)
