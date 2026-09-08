"""Who's free right now, where they are, and how long they'd take to
get somewhere.

The availability record this writes is read by Rook Supply, which uses
it to schedule gear servicing for windows when a responder isn't
likely to be called out. Supply only ever reads it — it never writes.
If you change the shape of what current_record() returns, tell the
Supply team before you ship it.
"""


def available_for(region, at):
    """Everyone marked available in this region at this moment.

    Availability is set by the responder or their handler in the app.
    Nothing in routing changes it.
    """
    ...


def travel_time_minutes(responder, location):
    """Estimated minutes for this responder to reach this location.

    Travel-time estimate, not straight-line distance — changed in 4.1.
    """
    ...


def current_record(responder):
    """The responder's current availability record.

    Read by Supply. Shape is a contract; see the note at the top of
    this file.
    """
    ...
