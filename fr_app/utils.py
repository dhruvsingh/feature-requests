from datetime import datetime
from collections import defaultdict

from fr_app.models import db, FeatureRequest
from marshmallow import ValidationError


def validate_date_in_future(value):
    """Validate date in future."""
    if value < datetime.now().date():
        raise ValidationError('Target date must be in the future')


def fix_client_priorities(new_client_priority):
    # TODO : make this more efficient
    """
    Fix client priority as per new client priority supplied by user at the time
    of creating a feature request.
    """
    all_frs = defaultdict()
    all_requests = FeatureRequest.query.all()

    for fr in all_requests:
        # update all_frs dict to key(the client_priority), values(fr_id)
        all_frs.setdefault(fr.client_priority, fr.id)

    # if new_client_priority is not yet set return
    if new_client_priority not in all_frs.keys():
        return

    # else fix priorities
    j = new_client_priority

    while j in all_frs.keys():
        j += 1

    # update
    while j > new_client_priority:
        fr_to_change = FeatureRequest.query.get(all_frs[j - 1])
        fr_to_change.client_priority = j
        db.session.add(fr_to_change)
        j -= 1

    db.session.commit()

    return
