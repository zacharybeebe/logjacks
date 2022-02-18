import json
from logjacks_app import app, db, request, render_template, redirect, url_for, session, flash, send_file
from logjacks_app.database.authentication import check_session, get_user, stands_to_database
from logjacks_app.config.constants import HELPFUL_SHEET_FUNCTIONS, FLASH_UNABLE_TO_IMPORT
from logjacks_app.data_etl.data_etl import get_stands_table, get_individual_table, get_attr_table
from logjacks_app.data_integrity.new_inventory import get_blank_row_json, read_imported_sheet, data_to_timber


@app.route('/<username>/dashboard')
def dashboard(username):
    if check_session(username, session):
        user = get_user(username)
        return render_template('private/dashboard.html', username=username)
    else:
        return redirect(url_for('login'))


@app.route('/<username>/new_inventory', methods=['POST', 'GET'])
def new_inventory(username):
    if check_session(username, session):
        user = get_user(username)
        blank_row = get_blank_row_json()
        table_data = None
        flash = None
        if request.method == 'POST':
            if request.files['inventory_file'].filename != '':
                print(f'{request.files=}')
                file = request.files['inventory_file']
                no_error, table_data = read_imported_sheet(file)
                if not no_error:
                    flash = FLASH_UNABLE_TO_IMPORT
            else:
                print(f'{request.form=}')
                data = eval(request.form['master|master_table'])
                if isinstance(data, dict):
                    stands = data_to_timber(data)
                    stands_to_database(user, stands)
                    return redirect(url_for('db_stands_summary', username=username))


                # x = eval(request.form['master|master_table'])
                # if isinstance(x, dict):
                #     for stand in x:
                #         print(stand)
                #         for key in x[stand]:
                #             print(f'\t{len(x[stand][key])} - {key}: {x[stand][key]}')
                #         print()


            # no_error, stand_data = check_new_stand(request.form)
            # if no_error:
            #     pass
            # else:
            #     pass
        return render_template('private/new_inventory.html', username=username, blank_row=blank_row, table_data=table_data,
                               flash=flash, helpful_func_text=HELPFUL_SHEET_FUNCTIONS)
    else:
        return redirect(url_for('login'))


@app.route('/<username>/stands', methods=['POST', 'GET'])
def db_stands(username):
    if check_session(username, session):
        user = get_user(username)
        stands = sorted([stand.name for stand in user.stands], key=lambda x: x.date_inventory)
        table_data = get_stands_table(user)
        return render_template('private/db_stands.html', username=username, table_data=table_data)
    else:
        return redirect(url_for('login'))


@app.route('/<username>/stands_summary', methods=['POST', 'GET'])
def db_stands_summary(username):
    if check_session(username, session):
        user = get_user(username)
        table_data = get_stands_table(user)
        return render_template('private/db_stands_summary.html', username=username, table_data=table_data)
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

        return render_template('private/db_individual1.html', username=username, stand=stand, plot=plot, tree=tree, log=log,
                               table_data=table_data, attr_table=attr_table)
    else:
        return redirect(url_for('login'))

# @app.route('/<username>/individual/<stand>', methods=['POST', 'GET'])
# def db_stand(username, stand):
#     table_data = None
#     attr_table = None
#     if check_session(username, session):
#         user = get_user(username)
#         stand_model = {stand_class.name: stand_class for stand_class in user.stands}[stand]
#         if not plot and not tree and not log:
#             attr_table = get_attr_table(stand_model)
#             table_data = get_individual_table(stand_model)
#         elif not tree and not log:
#             plot_model = {plot_class.number: plot_class for plot_class in stand_model.plots}[plot]
#             attr_table = get_attr_table(plot_model)
#             table_data = get_individual_table(plot_model)
#         elif not log:
#             plot_model = {plot_class.number: plot_class for plot_class in stand_model.plots}[plot]
#             tree_model = {tree_class.number: tree_class for tree_class in plot_model.trees}[tree]
#             attr_table = get_attr_table(tree_model)
#         else:
#             plot_model = {plot_class.number: plot_class for plot_class in stand_model.plots}[plot]
#             tree_model = {tree_class.number: tree_class for tree_class in plot_model.trees}[tree]
#             log_model = {log_class.number: log_class for log_class in tree_model.logs}[log]
#             attr_table = get_attr_table(log_model)
#
#         return render_template('private/db_stand.html', username=username, stand=stand,
#                                table_data=table_data, attr_table=attr_table)
#     else:
#         return redirect(url_for('login'))