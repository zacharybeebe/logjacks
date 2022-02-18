from datetime import (
    date,
    datetime
)
from hashlib import sha256
from logjacks_app import (
    app,
    db,
    User,
    Stand,
    Plot,
    Tree,
    Log
)


def get_user(username):
    return db.session.query(User).filter_by(username=username).first()


def check_session(username, session):
    try:
        if 'user' in session:
            if username == session['user']:
                return True
            else:
                return False
        else:
            return False
    except KeyError:
        return False


def check_create_account(request_form):
    initial_info = ['f_name', 'l_name', 'email', 'phone', 'company', 'username', 'password', 'password_confirm']
    fill_back_data = {}
    missing_data = False
    for i in initial_info:
        if i not in ['password', 'password_confirm']:
            fill_back_data[i] = request_form[i]
        if request_form[i] == '':
            missing_data = True
    if missing_data:
        return True, fill_back_data, 'Missing Data'
    else:
        if db.session.query(User).filter_by(username=request_form['username']).first() is not None:
            fill_back_data['username'] = ''
            return True, fill_back_data, 'Username Taken'

        elif db.session.query(User).filter_by(email=request_form['email']).first() is not None:
            fill_back_data['email'] = ''
            return True, fill_back_data, 'Email Already In Use'

        elif request_form['password'] != request_form['password_confirm']:
            return True, fill_back_data, 'Passwords Do Not Match'

        else:
            fill_back_data['password'] = request_form['password']
            user = User(**fill_back_data)
            db.session.add(user)
            db.session.commit()
            return False, None, user


def check_login(username, password):
    if username == '':
        return False, 'Please Enter a Username'
    else:
        user = get_user(username)
        if not user:
            return False, 'Incorrect Username'
        if user.password != sha256(password.encode('utf-8')).hexdigest():
            return False, 'Incorrect Password'
        else:
            return True, user


def initialize_user(user, session):
    username = user.username
    session['user'] = username
    session['date'] = [date.today().year, date.today().month]
    session['db_stand'] = None
    session['db_plot'] = None
    session['db_tree'] = None
    session['fvs_stand'] = None
    session.permanent = True


def disengage_user(session):
    session.pop('user', None)
    session.pop('date', None)



""" 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    stand_id = db.Column(db.Integer, db.ForeignKey('stand.id'), nullable=False)
    plot_id = db.Column(db.Integer, db.ForeignKey('plot.id'), nullable=False)
    tree_id = db.Column(db.Integer, db.ForeignKey('tree.id'), nullable=False)
    species = db.Column(db.String(4), db.ForeignKey('tree.species'), nullable=False)

    number = db.Column(db.Integer)
    stem_height = db.Column(db.Integer)
    length = db.Column(db.Integer)
    defect = db.Column(db.Integer)

    lpa = db.Column(db.Float)
    top_dib = db.Column(db.Integer)
    grade = db.Column(db.String(4))
    grade_name = db.Column(db.String(32))
    scrib = db.Column(db.Float)
    bf = db.Column(db.Float)
    cf = db.Column(db.Float)
    bf_ac = db.Column(db.Float)
    cf_ac = db.Column(db.Float)

    logs = db.relationship('Tree', secondary=tree_logs, backref=db.backref('logs', lazy=True))

"""

def stands_to_database(user, stands):
    for stand in stands:
        db_stand = Stand(user_id=user.id, name=stand.name, acres=stand.acres, date_inventory=stand.date_inventory)
        db.session.add(db_stand)
        db.session.commit()

        for i, plot in enumerate(stand.plots, 1):
            db_plot = Plot(user_id=user.id, stand_id=db_stand.id, number=i, plot_factor=plot.plot_factor)
            db.session.add(db_plot)
            db.session.commit()

            for j, tree in enumerate(plot.trees, 1):
                db_tree = Tree(user_id=user.id, stand_id=db_stand.id, plot_id=db_plot.id, plot_factor=db_plot.plot_factor,
                               number=j, species=tree.species, dbh=tree.dbh, total_height=tree.total_height, hdr=tree.hdr,
                               ba=tree.ba, rd=tree.rd, tpa=tree.tpa, ba_ac=tree.ba_ac, rd_ac=tree.rd_ac, stem_dibs=tree.stem_dibs,
                               dib_heights=tree.dib_heights, merch_dib=tree.merch_dib, merch_height=tree.merch_height,
                               bf=tree.bf, cf=tree.cf, bf_ac=tree.bf_ac, cf_ac=tree.cf_ac, vbar=tree.vbar)
                db.session.add(db_tree)
                db.session.commit()

                for k, log in tree.logs.items():
                    db_log = Log(user_id=user.id, stand_id=db_stand.id, plot_id=db_plot.id, tree_id=db_tree.id,
                                 species=log.species, number=k, stem_height=log.stem_height, length=log.length, defect=log.defect,
                                 lpa=log.lpa, top_dib=log.top_dib, grade=log.grade, grade_name=log.grade_name, scrib=log.scrib,
                                 bf=log.bf, cf=log.cf, bf_ac=log.bf_ac, cf_ac=log.cf_ac)
                    db.session.add(db_log)
                    db.session.commit()

                    db_tree.logs.append(db_log)
                db_plot.trees.append(db_tree)
            db_stand.plots.append(db_plot)
        user.stands.append(db_stand)
    db.session.commit()





# def check_update_user_account(username, session, request_form):
#     user = get_user(username)
#     old_username = (username, )
#     old_email = (user.email, )
#
#     if request_form['username'] != old_username[0]:
#         if db.session.query(User).filter_by(username=request_form['username']).first():
#             return False, None, [False, 'Cannot change username as it already exists']
#     if request_form['email'] != old_email[0]:
#         if db.session.query(User).filter_by(email=request_form['email']).first():
#             return False, None, [False, 'Cannot change email as it is already in use']
#
#     address = ['street', 'apt_num', 'city', 'state', 'zip']
#     addy = {}
#     for key in request_form:
#         if key not in address:
#             if key != 'delete_account':
#                 if request_form[key] == '':
#                     return False, None, [False, f'*{key.capitalize()}* cannot be blank']
#         else:
#             addy[key] = request_form[key]
#
#     user.name = request_form['name']
#     user.email = request_form['email']
#     user.phone = request_form['phone']
#     user.company = request_form['company']
#     user.state = request_form['state_id']
#     user.metro = request_form['metro']
#     user.username = request_form['username']
#     user.password = request_form['password']
#     user.address = addy
#
#     if request_form['username'] != old_username[0]:
#         session['user'] = user.username
#
#     db.session.commit()
#     app.logger.info(f'{user.username} account update success')
#     return True, user, [True, 'Account Updated Successfully']


# def delete_user(username, session):
#     user = get_user(username)
#     username = (user.username, )
#     if user.type == 'pro':
#         interested_jobs = list(user.interested)
#         for job in interested_jobs:
#             job.interested.remove(user)
#
#         master = {}
#         scheduled_jobs = list(user.scheduled)
#         for job in scheduled_jobs:
#             job.status = 'posted'
#             job.pro_id = -1
#             client = job.get_client(job.client_id)
#             if client.username not in master:
#                 master[client.username] = {'scheduled': {},
#                                            'completed': {}}
#             master[client.username]['scheduled'][job.id] = {'Job Type: ': JOB_NAME_KEYS[job.type],
#                                                             'Price: ': format_price(job.price),
#                                                             'Scheduled Date: ': format_date(job.date_assigned)}
#
#         completed_jobs = list(user.completed)
#         for job in completed_jobs:
#             job.pro_id = -2
#             client = job.get_client(job.client_id)
#             if client.username not in master:
#                 master[client.username] = {'scheduled': {},
#                                            'completed': {}}
#             master[client.username]['completed'][job.id] = {'Job Type: ': JOB_NAME_KEYS[job.type],
#                                                             'Completed Date: ': format_date(job.date_assigned)}
#
#         for notif in user.notification_deleted_pro(user.username, master):
#             db.session.add(notif)
#     else:
#         master = {}
#         posted_jobs = list(user.posted)
#         for job in posted_jobs:
#             for pro in job.interested:
#                 if pro.username not in master:
#                     master[pro.username] = {'interested': {},
#                                             'scheduled': {},
#                                             'completed': {}}
#                 master[pro.username]['interested'][job.id] = {'Job Type: ': JOB_NAME_KEYS[job.type],
#                                                               'Price: ': format_price(job.price),
#                                                               'Scheduled Date: ': format_date(job.date_assigned)}
#             db.session.delete(job)
#
#         scheduled_jobs = list(user.scheduled)
#         for job in scheduled_jobs:
#             pro = job.get_pro(job.pro_id)
#             if pro.username not in master:
#                 master[pro.username] = {'interested': {},
#                                         'scheduled': {},
#                                         'completed': {}}
#             master[pro.username]['scheduled'][job.id] = {'Job Type: ': JOB_NAME_KEYS[job.type],
#                                                          'Price: ': format_price(job.price),
#                                                          'Scheduled Date: ': format_date(job.date_assigned)}
#             db.session.delete(job)
#
#         completed_jobs = list(user.completed)
#         for job in completed_jobs:
#             job.client_id = -1
#             pro = job.get_pro(job.pro_id)
#             if pro.username not in master:
#                 master[pro.username] = {'interested': {},
#                                         'scheduled': {},
#                                         'completed': {}}
#             master[pro.username]['completed'][job.id] = {'Job Type: ': JOB_NAME_KEYS[job.type],
#                                                          'Completed Date: ': format_date(job.date_assigned)}
#
#         for notif in user.notification_deleted_pro(user.username, master):
#             db.session.add(notif)
#
#     for friend in user.friends:
#         friend.friends.remove(user)
#
#     for notif in list(user.sent_notifications):
#         notif.sender_id = -1
#
#     for notif in list(user.received_notifications):
#         notif.receiver_id = -1
#
#     db.session.delete(user)
#     db.session.commit()
#     session.pop('user', None)
#     session.pop('date', None)
#     session.pop('missing_link', None)
#     app.logger.info(f'{username[0]} deleted account successfully')