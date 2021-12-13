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


def get_db_table(user, table):
    return DB_TABLE_FUNCS[table](user)


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
