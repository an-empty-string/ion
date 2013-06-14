from flask import flash, redirect, url_for, session
import hashlib
import i3
import i3.models

# Auth helper functions
def is_valid_login(username, password):
    passwd_hash = hashlib.sha256(password).hexdigest()
    matching = i3.models.User.query.filter(
            i3.models.User.username == username,
            i3.models.User.passwd_hash == passwd_hash).all()
    if len(matching) == 1:
        return (username, matching[0].uid)
    return False

def is_in_group(perm):
    try: matching = i3.models.UserPermissionMapItem.query.filter(
            i3.models.UserPermissionMapItem.uid == session["uid"],
            i3.models.UserPermissionMapItem.permission == perm).all()
    except: return False
    if len(matching) != 0:
        return True
    return False

def require_permission(perm):
    if not is_in_group(perm):
        flash("You do not have the required permissions!", "error")
        return redirect(url_for('auth_login'))

@i3.app.context_processor
def inject_helpers():
    return dict(is_in_group = is_in_group)
