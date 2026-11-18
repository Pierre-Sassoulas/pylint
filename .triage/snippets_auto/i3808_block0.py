from datetime import datetime, timedelta as td


see_you = {
    'now': lambda: datetime.utcnow().isoformat(),  # it's ok
    'next_time': lambda: (datetime.utcnow() + td(hours=6)).isoformat(),  # false positive
}
