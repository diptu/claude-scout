"""Project exceptions. Deliberately thin: stages report errors as counts in
their run() summaries rather than raising, so only genuinely unrecoverable
states belong here."""


class ScoutError(Exception):
    """Base class for claude-scout errors."""
