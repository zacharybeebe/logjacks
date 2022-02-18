from logjacks_app.data_etl.data_etl_conifg import *
from time import perf_counter


def _timer_(func):
    def wrapper(*args, **kwargs):
        now = perf_counter()
        x = func(*args, **kwargs)
        after = perf_counter()
        print(f'{func.__name__} took {round(after-now, 10)} seconds\n')
        return x
    return wrapper


def get_stands_table(user):
    table_data = [list(DB_STAND.keys())]
    for stand in user.stands:
        stand_info = {
            'stand_data': [DB_STAND[key](stand) for key in DB_STAND],
            'plots': {
                'header': list(DB_PLOT.keys())
            }
        }
        for plot in stand.plots:
            plot_info = {
                'plot_data': [DB_PLOT[key](plot) for key in DB_PLOT],
                'trees': {
                    'header': list(DB_TREE.keys()),
                }
            }
            for tree in plot.trees:
                tree_info = {
                    'tree_data': [DB_TREE[key](tree) for key in DB_TREE],
                    'logs': {
                        'header': list(DB_LOG.keys())
                    }
                }
                for log in tree.logs:
                    log_info = {
                        'log_data': [DB_LOG[key](log) for key in DB_LOG]
                    }
                    tree_info['logs'][log.number] = log_info
                plot_info['trees'][tree.number] = tree_info
            stand_info['plots'][plot.number] = plot_info
        table_data.append(stand_info)
    return table_data


def get_individual_table(model):
    table = [TABLE_HEADS]
    summary = SUMMARY_FUNCS[model.__class__.__name__](model)
    for spp in summary:
        temp = [spp.upper()]
        for key in summary[spp]:
            temp.append(f_round_or_blank(summary[spp][key]))
        table.append(temp)
    return table


def get_attr_table(model):
    attrs = {}
    ref = model.__class__.__name__
    for key in ATTR_TABLES[ref]:
        attrs[key] = ATTR_TABLES[ref][key](model)
    return attrs
