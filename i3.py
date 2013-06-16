from i3 import app
from i3.views import news, auth, umanage
GP = ["GET", "POST"]
## Configuration
DEFAULT_VIEW = news.news_read
## URL Rules
app.add_url_rule('/', view_func = DEFAULT_VIEW)
## News
app.add_url_rule('/news/', view_func = news.news_read)
app.add_url_rule('/news/<int:pid>/', 
        view_func = news.news_read_post)
app.add_url_rule('/news/post/', view_func = news.news_post,
        methods = GP)
app.add_url_rule('/news/edit/<int:pid>/', view_func = news.news_edit,
        methods = GP)
app.add_url_rule('/news/delete/<int:pid>/',
        view_func = news.news_delete, methods = GP)
app.add_url_rule('/api/news/', view_func = news.api_news_read)
app.add_url_rule('/api/news/setread/<int:pid>/', 
        view_func = news.api_news_set_read)
app.add_url_rule('/api/news/setunread/<int:pid>/',
        view_func = news.api_news_set_unread)
app.add_url_rule('/api/news/numberunread/',
        view_func = news.api_news_total_unread)
## User Management
app.add_url_rule('/userman/list/', view_func = umanage.list_users)
app.add_url_rule('/userman/listperms/<int:uid>/', 
        view_func = umanage.list_perms)
app.add_url_rule('/api/userman/create/', view_func=umanage.create_user,
        methods = ["POST"])
app.add_url_rule('/api/userman/delete/', view_func=umanage.delete_user,
        methods = ["POST"])
app.add_url_rule('/api/userman/addperm/', 
        view_func = umanage.add_perm, methods = ["POST"])
app.add_url_rule('/api/userman/delperm/',
        view_func = umanage.del_perm, methods = ["POST"])
## Auth
app.add_url_rule('/login/', view_func = auth.auth_login, methods=GP)
app.add_url_rule('/logout/', view_func = auth.auth_logout)
app.add_url_rule('/api/login/', view_func = auth.api_auth_login, 
        methods=GP)
app.add_url_rule('/api/whoami/', view_func = auth.api_auth_whoami)
app.add_url_rule('/api/logout/', view_func = auth.api_auth_logout)
app.run(debug = True)
