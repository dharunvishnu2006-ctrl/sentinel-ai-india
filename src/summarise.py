import re


def build_context(events):
    lines = []
    for e in events:
        lines.append(f"agent={e['agent']} kind={e['kind']} " f"payload={e['payload']}")
    return "\n".join(lines)


def build_prompt(events):
    context = build_context(events)
    return (
        "Summarise these incident events in exactly 3 sentences, "
        "plus one recommended action. Use ONLY the facts below. "
        "If something is not present in the facts, write "
        "'not available' rather than inventing it.\n\n"
        f"FACTS:\n{context}"
    )


def extract_numbers(text):
    return set(re.findall(r"\d+", text))


def extract_known_names(text, known_names):
    found = set()
    for name in known_names:
        if name in text:
            found.add(name)
    return found


def verify_summary(summary, events, known_agents):
    context = build_context(events)

    summary_numbers = extract_numbers(summary)
    context_numbers = extract_numbers(context)
    unverified_numbers = summary_numbers - context_numbers

    summary_agents = extract_known_names(summary, known_agents)
    mentioned_agents_in_events = {e["agent"] for e in events}
    unverified_agents = summary_agents - mentioned_agents_in_events

    if unverified_numbers or unverified_agents:
        return {
            "verified": False,
            "unverified_numbers": unverified_numbers,
            "unverified_agents": unverified_agents,
        }
    return {"verified": True}
