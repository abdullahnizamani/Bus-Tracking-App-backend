# utils.py
from .models import ActivityLog

def log_system_activity(user, action, description, level='info'):
    """
    Helper function to easily create an audit log from any view.
    """
    # If the user isn't authenticated (e.g., an automated system task), user will be None
    if user and not user.is_authenticated:
        user = None
        
    ActivityLog.objects.create(
        user=user,
        action=action,
        description=description,
        level=level
    )