from flask import render_template, request, redirect, url_for, \
        flash, jsonify, session
import i3
import i3.database
import i3.decorators
import i3.models
import time

# Helpers
@i3.app.template_filter('truncate120')
def truncate120(s):
    return str(s[:120]) + ("..." if len(s) > 120 else "")

@i3.app.template_filter('truncate30')
def truncate30(s):
    return str(s[:25]) + ("..." if len(s) > 25 else "")

@i3.app.template_filter('breaks2html')
def breaks2html(s):
    return s.replace("\n", "<br>")

def has_read_item(pid):
    try:
        x = i3.models.NewsReadMapItem.query.filter(
                i3.models.NewsReadMapItem.uid == session["uid"],
                i3.models.NewsReadMapItem.pid == pid).all()
        if len(x) > 0:
            return True
    except Exception, e:
        print e
    return False

def total_unread_items():
    try:
        read = i3.models.NewsReadMapItem.query.filter(
                i3.models.NewsReadMapItem.uid == session["uid"]
                ).all()
        items = i3.models.NewsPost.query.all()
        n = len(items) - len(read)
        if n > 0: return str(n)
        else: return ""
    except Exception, e: 
        return ""

@i3.app.context_processor
def add_has_read():
    return dict(has_read_item=has_read_item,
            total_unread_items = total_unread_items,
            ctime = time.ctime
            )

def r():
    if "uid" in session: return False
    return redirect(url_for("auth_login"))

# User interface
def news_read():
    if r(): return r()
    posts = i3.models.NewsPost.query.all()[::-1]
    return render_template("news/read.html", posts = posts)

def news_read_post(pid):
    if r(): return r()
    posts = i3.models.NewsPost.query.filter(
            i3.models.NewsPost.pid == pid)
    return render_template("news/read.html", posts = posts)

def news_post():
    x = i3.auth.require_permission("admin_news")
    if x: return x
    try:
        title = request.form["title"]   
        contents = request.form["contents"]
        post = i3.models.NewsPost(title, contents, time_posted = time.time())
        i3.database.db_session.add(post)
        i3.database.db_session.commit()
        flash("News posted.", "success")
    except Exception, e:
        flash("There was an error posting news.\n%s" % repr(e), "error")
    finally:
        return redirect(url_for("news_read"))

def news_edit(pid):
    x = i3.auth.require_permission("admin_news")
    if x: return x
    if request.method == "GET":
        post = i3.models.NewsPost.query.filter(
                i3.models.NewsPost.pid == pid).first()
        title = post.title
        contents = post.contents
        return render_template("news/editmodal.html", pid = pid, 
                title = title, contents = contents)
    try:
        title = request.form["title"]
        contents = request.form["contents"]
        post = i3.models.NewsPost.query.filter(
                i3.models.NewsPost.pid == pid).first()
        post.title = title
        post.contents = contents
        i3.database.db_session.commit()
        flash("News post edited.", "success")
    except Exception, e:
        flash("An error occured.\n%s" % repr(e), "error")
    return redirect(url_for("news_read"))

def news_delete(pid): 
    x = i3.auth.require_permission("admin_news")
    if x: return x
    try:
        q = i3.models.NewsPost.query.filter(
                i3.models.NewsPost.pid == pid).first()
        i3.database.db_session.delete(q)
        i3.database.db_session.commit()
        flash("Post deleted.", "success")
    except:
        flash("An error occurred!", "error")
    return redirect(url_for("news_read"))

# API for news
def api_news_read():
    if r(): return r()
    posts = i3.models.NewsPost.query.all()[::-1]
    posts = [{"title": str(i.title), "contents": i.contents} for i in
            posts]
    return jsonify(posts=posts)

def api_news_set_read(pid):
    if "uid" in session:
        mapitem = i3.models.NewsReadMapItem(session["uid"], pid)
        i3.database.db_session.add(mapitem)
        i3.database.db_session.commit()
        return jsonify(success = True)
    else:
        return jsonify(success = False, error = "notloggedin")

def api_news_set_unread(pid):
    if "uid" in session:
        mapitem = i3.models.NewsReadMapItem.query.filter(
                i3.models.NewsReadMapItem.uid == session["uid"],
                i3.models.NewsReadMapItem.pid == pid).first()
        i3.database.db_session.delete(mapitem)
        i3.database.db_session.commit()
        return jsonify(success = True)
    else:
        return jsonify(success = False, error = "notloggedin")

def api_news_total_unread():
    return render_template("news/unread.html")
