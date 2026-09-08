"""Putting the offer on somebody's phone and waiting for an answer.

We work down the ranked list one at a time. Each responder gets the
callout and a fixed window to answer. If they take it we're done. If
they don't, we move on.
"""

import time

from config import OFFER_TIMEOUT_SECONDS
import history
import routing

ACCEPTED = "accepted"
DECLINED = "declined"
NO_ANSWER = "no_answer"


def dispatch(callout):
    """Offer a callout down the ranked list until somebody takes it.

    Returns the responder who took it, or None if we got to the bottom
    of the list without a yes.
    """
    for responder in routing.rank_for_callout(callout):
        answer = offer_to(responder, callout)
        if answer == ACCEPTED:
            history.record_accepted(responder)
            return responder
        history.record_declined(responder)
    return None


def offer_to(responder, callout):
    """Push the callout to a responder's phone and wait for a tap.

    Returns ACCEPTED, DECLINED or NO_ANSWER. Everything downstream
    treats the last two the same way: we asked, and we didn't get a
    yes.
    """
    push_to_device(responder, callout)
    deadline = time.time() + OFFER_TIMEOUT_SECONDS
    while time.time() < deadline:
        answer = poll_device(responder, callout)
        if answer is not None:
            return answer
    withdraw_from_device(responder, callout)
    return NO_ANSWER


def push_to_device(responder, callout):
    """Send the offer to whatever device they're signed in on."""
    ...


def poll_device(responder, callout):
    """Has this responder answered yet? None if they haven't."""
    ...


def withdraw_from_device(responder, callout):
    """Take the offer off their phone. It's gone to somebody else."""
    ...
