"""Ranking available responders for a single callout.

Given a callout and everyone who's currently free, work out the order
we should ask them in. Top of the list gets asked first; if they don't
take it, we move down.
"""

from config import (
    WEIGHT_PROXIMITY,
    WEIGHT_RECENT_ACCEPTANCE,
    WEIGHT_CAPABILITY_MATCH,
    PROXIMITY_HORIZON_MINUTES,
)
import availability
import history


def rank_for_callout(callout):
    """Every available responder, best match first.

    Nobody is removed here. Ranking decides the order we ask in, not
    whether we ask at all.
    """
    candidates = availability.available_for(callout.region, callout.at)
    scored = [(score(r, callout), r) for r in candidates]
    scored.sort(key=lambda pair: pair[0], reverse=True)
    return [responder for _, responder in scored]


def score(responder, callout):
    """How good a match this responder is for this callout.

    Higher is better. Three parts, each weighted:
      - how fast they can get there
      - how often they've been taking callouts lately
      - whether they can do this kind of work at all
    """
    return (
        WEIGHT_PROXIMITY * proximity_score(responder, callout)
        + WEIGHT_RECENT_ACCEPTANCE * history.recent_acceptance(responder)
        + WEIGHT_CAPABILITY_MATCH * capability_score(responder, callout)
    )


def proximity_score(responder, callout):
    """1.0 if they're practically there already, falling off with
    travel time, 0.0 past the horizon.

    Travel time, not straight-line distance. That changed in 4.1.
    """
    minutes = availability.travel_time_minutes(responder, callout.location)
    if minutes >= PROXIMITY_HORIZON_MINUTES:
        return 0.0
    return 1.0 - (minutes / PROXIMITY_HORIZON_MINUTES)


def capability_score(responder, callout):
    """1.0 if they can do everything this callout needs, 0.0 if they
    can't do any of it, somewhere in between otherwise.
    """
    needed = set(callout.required_capabilities)
    if not needed:
        return 1.0
    matched = needed & set(responder.capabilities)
    return len(matched) / len(needed)
