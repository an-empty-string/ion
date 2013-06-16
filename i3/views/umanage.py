from flask import render_template, request, redirect, url_for, \
        flash, jsonify, session
import i3
import i3.auth
import i3.database
import i3.models
import hashlib

def create_user():
    x = i3.auth.require_permission("admin_user")
    if x: return x
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        passwd_hash = hashlib.sha256(password).hexdigest()
        user = i3.models.User(username, passwd_hash)
        i3.database.db_session.add(user)
        i3.database.db_session.commit()
    return jsonify(success=True)

def delete_user():
    x = i3.auth.require_permission("admin_user")
    if x: return x
    if request.method == "POST":
        uid = request.form["uid"]
        i3.database.db_session.delete(i3.models.User.query.filter(
                i3.models.User.uid == uid
                ).first())
        i3.database.db_session.commit()
    return jsonify(success=True) 

def add_perm():
    x = i3.auth.require_permission("admin_user")
    if x: return x
    if request.method == "POST":
        uid = request.form["uid"]
        permission = request.form["permission"]
        i3.database.db_session.add(i3.models.UserPermissionMapItem(
            uid, permission))
        i3.database.db_session.commit()
    return jsonify(success=True)

def del_perm():
    x = i3.auth.require_permission("admin_user")
    if x: return x
    if request.method == "POST":
        mapid = request.form["mapid"]
        i3.database.db_session.delete(
                i3.models.UserPermissionMapItem.query.filter(
                    i3.models.UserPermissionMapItem.mapid == mapid
                    ).first()
                )
        i3.database.db_session.commit()
    return jsonify(success=True)

def list_users():
    x = i3.auth.require_permission("admin_user")
    if x: return x
    return render_template("uman/list.html",
        users = i3.models.User.query.all())

def list_perms(uid):
    x = i3.auth.require_permission("admin_user")
    if x: return x
    perms = i3.models.UserPermissionMapItem.query.filter(
        i3.models.UserPermissionMapItem.uid == uid
        ).all()
    return render_template("uman/listp.html", perms = perms, 
            uid = uid)
