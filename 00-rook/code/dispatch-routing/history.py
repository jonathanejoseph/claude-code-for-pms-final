"""Recent acceptance — a running score of how often somebody has been
taking the callouts we send them.

One of the three inputs to ranking. Sits between 0 and 1. Everyone
starts at NEUTRAL_SCORE when we take them on.
"""

from config import (
    ACCEPTANCE_CREDIT,
    DECLINE_PENALTY,
    SCORE_FLOOR,
    SCORE_CEILING,
)

NEUTRAL_SCORE = 0.5

_scores = {}


def recent_acceptance(responder):
    """This responder's score right now. Read by routing.score()."""
    return _scores.get(responder.id, NEUTRAL_SCORE)


def record_accepted(responder):
    """They took the callout. Score goes up."""
    _set(responder, recent_acceptance(responder) + ACCEPTANCE_CREDIT)


# TODO(wen, 2019): should this ease back toward NEUTRAL_SCORE on its
# own after a while? For: somebody who had a bad month shouldn't still
# be carrying it in the spring. Against: if somebody has stopped taking
# work, we probably want that to stick until they take work again.
# Leaving it as-is for now.
def record_declined(responder):
    """They turned it down, or we ran out of time waiting. Score goes
    down. Same either way — we asked and we didn't get a yes.
    """
    _set(responder, recent_acceptance(responder) - DECLINE_PENALTY)


def _set(responder, value):
    _scores[responder.id] = max(SCORE_FLOOR, min(SCORE_CEILING, value))
