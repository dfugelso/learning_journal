from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from pyramid.httpexceptions import HTTPNotFound, HTTPFound

from pyramid.security import authenticated_userid
from pyramid.security import forget, remember

from .forms import  (
    EntryCreateForm,
    EntryEditForm,
)

from .models import (
    DBSession,
    MyModel,
    Entry,
    User,
    )

from .forms import LoginForm



# @view_config(route_name='home', renderer='templates/mytemplate.pt')
# def my_view(request):
    # try:
        # one = DBSession.query(MyModel).filter(MyModel.name == 'one').first()
    # except DBAPIError:
        # return Response(conn_err_msg, content_type='text/plain', status_int=500)
    # return {'one': one, 'project': 'learning_journal'}

@view_config(route_name='home', renderer='templates/list.jinja2')
def index_page(request):
    '''
    Root page gets all entries and display them.
    '''
    form = None
    if not authenticated_userid(request):
        form = LoginForm()
    entries = Entry.all()
    return {'entries': entries, 'login_form': form}

@view_config(route_name='detail', renderer='templates/detail.jinja2')
def view(request):
    '''
    Show the detail of one entry.
    '''
    this_id = request.matchdict.get('id', -1)
    entry = Entry.by_id(this_id)
    if not entry:
        return HTTPNotFound()
    return {'entry': entry}


@view_config(route_name='action', match_param='action=create', renderer='templates/edit.jinja2', permission='create')
def create(request):
    ''' 
    Create a new entry.
    '''
    entry = Entry()
    form = EntryCreateForm(request.POST)
    if request.method == 'POST' and form.validate():
        form.populate_obj(entry)
        DBSession.add(entry)
        return HTTPFound(location=request.route_url('home'))
    return {'form': form, 'action': request.matchdict.get('action')}

@view_config(route_name='action', match_param='action=edit', renderer='templates/edit.jinja2', permission='edit')
def update(request):
    '''
    Allow user to edit a page.
    '''
    id = int(request.params.get('id', -1))
    entry = Entry.by_id(id)
    if not entry:
        return HTTPNotFound()
    form = EntryEditForm(request.POST, entry)
    if request.method == 'POST' and form.validate():
        form.populate_obj(entry)
        return HTTPFound(location=request.route_url('detail', id=entry.id))
    return {'form': form, 'action': request.matchdict.get('action')}

@view_config(route_name='auth', match_param='action=in', renderer='string', request_method='POST')
def sign_in(request):
    login_form = None
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
    if login_form and login_form.validate():
        user = User.by_name(login_form.username.data)
        if user and user.verify_password(login_form.password.data):
            headers = remember(request, user.name)
        else:
            headers = forget(request)
    else:
        headers = forget(request)
    return HTTPFound(location=request.route_url('home'), headers=headers)

