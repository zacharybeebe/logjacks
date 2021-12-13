from logjacks_app import app, db, request, render_template, redirect, url_for, session, flash, send_file
from logjacks_app.database.authentication import check_session, get_user
from logjacks_app.data_etl.data_etl import get_db_table, get_individual_table, get_attr_table


@app.route('/<username>/dashboard')
def dashboard(username):
    if check_session(username, session):
        user = get_user(username)
        return render_template('private/dashboard.html', username=username)
    else:
        return redirect(url_for('login'))


@app.route('/<username>/tables/<table>', methods=['POST', 'GET'])
def db_tables(username, table):
    if check_session(username, session):
        user = get_user(username)
        table_data = get_db_table(user, table)
        return render_template('private/db_tables.html', username=username, table=table, table_data=table_data)
    else:
        return redirect(url_for('login'))


@app.route('/<username>/individual/<stand>_<int:plot>_<int:tree>_<int:log>', defaults={'plot': 0, 'tree': 0, 'log': 0}, methods=['POST', 'GET'])
@app.route('/<username>/individual/<stand>_<int:plot>_<int:tree>_<int:log>', defaults={'tree': 0, 'log': 0}, methods=['POST', 'GET'])
@app.route('/<username>/individual/<stand>_<int:plot>_<int:tree>_<int:log>', defaults={'log': 0}, methods=['POST', 'GET'])
@app.route('/<username>/individual/<stand>_<int:plot>_<int:tree>_<int:log>', methods=['POST', 'GET'])
def db_individual(username, stand, plot, tree, log):
    table_data = None
    attr_table = None
    if check_session(username, session):
        user = get_user(username)
        stand_model = {stand_class.name: stand_class for stand_class in user.stands}[stand]
        if not plot and not tree and not log:
            attr_table = get_attr_table(stand_model)
            table_data = get_individual_table(stand_model)
        elif not tree and not log:
            plot_model = {plot_class.number: plot_class for plot_class in stand_model.plots}[plot]
            attr_table = get_attr_table(plot_model)
            table_data = get_individual_table(plot_model)
        elif not log:
            plot_model = {plot_class.number: plot_class for plot_class in stand_model.plots}[plot]
            tree_model = {tree_class.number: tree_class for tree_class in plot_model.trees}[tree]
            attr_table = get_attr_table(tree_model)
        else:
            plot_model = {plot_class.number: plot_class for plot_class in stand_model.plots}[plot]
            tree_model = {tree_class.number: tree_class for tree_class in plot_model.trees}[tree]
            log_model = {log_class.number: log_class for log_class in tree_model.logs}[log]
            attr_table = get_attr_table(log_model)

        return render_template('private/db_individual.html', username=username, stand=stand, plot=plot, tree=tree, log=log,
                               table_data=table_data, attr_table=attr_table)
    else:
        return redirect(url_for('login'))
