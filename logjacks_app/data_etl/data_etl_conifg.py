from logjacks_app.utils.formatting import f_round_or_blank, h_date

DB_STAND = {
    'Name': lambda stand: stand.name,
    'Acres': lambda stand: stand.acres,
    'Plots': lambda stand: len(list(stand.plots)),
    'Trees': lambda stand: sum([len(list(plot.trees)) for plot in stand.plots]),
    'Date': lambda stand: stand.date_inventory,
    'Preferred Log Length': lambda stand: stand.pref_log_length,
    'Minimum Log Length': lambda stand: stand.min_log_length,
    'Utility Log DIB': lambda stand: stand.util_log_dib,
    'TPA': lambda stand: f_round_or_blank(stand.tpa) if stand.tpa > 0 else 'No Plots',
    'BA/AC': lambda stand: f_round_or_blank(stand.ba_ac),
    'QMD': lambda stand: f_round_or_blank(stand.qmd),
    'RD/AC': lambda stand: f_round_or_blank(stand.rd_ac),
    'BF/AC': lambda stand: f_round_or_blank(stand.bf_ac),
    'CF/AC': lambda stand: f_round_or_blank(stand.cf_ac),
    'VBAR': lambda stand: f_round_or_blank(stand.vbar)
}


DB_PLOT = {
    'Plot Number': lambda plot: plot.number,
    'Plot Factor': lambda plot: plot.plot_factor,
    'Trees': lambda plot: plot.tree_count,
    'TPA': lambda plot: f_round_or_blank(plot.tpa) if plot.tpa > 0 else 'No Trees',
    'BA/AC': lambda plot: f_round_or_blank(plot.ba_ac),
    'QMD': lambda plot: f_round_or_blank(plot.qmd),
    'RD/AC': lambda plot: f_round_or_blank(plot.rd_ac),
    'BF/AC': lambda plot: f_round_or_blank(plot.bf_ac),
    'CF/AC': lambda plot: f_round_or_blank(plot.cf_ac),
    'VBAR': lambda plot: f_round_or_blank(plot.vbar)
}


DB_TREE = {
    'Tree Number': lambda tree: tree.number,
    'Species': lambda tree: tree.species,
    'DBH': lambda tree: tree.dbh,
    'Total Height': lambda tree: f_round_or_blank(tree.total_height),
    'HDR': lambda tree: f_round_or_blank(tree.hdr),
    'BA': lambda tree: round(tree.ba, 2),
    'RD': lambda tree: round(tree.rd, 2),
    'TPA': lambda tree: f_round_or_blank(tree.tpa),
    'BA/AC': lambda tree: f_round_or_blank(tree.ba_ac),
    'RD/AC': lambda tree: f_round_or_blank(tree.rd_ac),
    'Merch DIB': lambda tree: tree.merch_dib,
    'Merch Height': lambda tree: tree.merch_height,
    'BF': lambda tree: f_round_or_blank(tree.bf),
    'CF': lambda tree: f_round_or_blank(tree.cf),
    'BF/AC': lambda tree: f_round_or_blank(tree.bf_ac),
    'CF/AC': lambda tree: f_round_or_blank(tree.cf_ac),
    'VBAR': lambda tree: f_round_or_blank(tree.vbar)
}

DB_LOG = {
    'Log Number': lambda log: log.number,
    'Stem Height': lambda log: log.stem_height,
    'Length': lambda log: log.length,
    'Defect': lambda log: log.defect,
    'Species': lambda log: log.species,
    'Logs/AC': lambda log: f_round_or_blank(log.lpa),
    'Top DIB': lambda log: log.top_dib,
    'Grade': lambda log: log.grade,
    'BF': lambda log: f_round_or_blank(log.bf),
    'CF': lambda log: f_round_or_blank(log.cf),
    'BF/AC': lambda log: f_round_or_blank(log.bf_ac),
    'CF/AC': lambda log: f_round_or_blank(log.cf_ac)
}


def _get_stands_table(user):
    table_data = [list(DB_STAND.keys())]
    for stand in user.stands:
        table_data.append([DB_STAND[key](stand) for key in DB_STAND])
    return table_data


def _get_plots_table(user):
    table_data = [['Stand Name'] + list(DB_PLOT.keys())]
    for stand in user.stands:
        for plot in stand.plots:
            temp = [stand.name] + [DB_PLOT[key](plot) for key in DB_PLOT]
            table_data.append(temp)
    return table_data


def _get_trees_table(user):
    table_data = [['Stand Name', 'Plot Number'] + list(DB_TREE.keys())]
    for stand in user.stands:
        for plot in stand.plots:
            for tree in plot.trees:
                temp = [stand.name, plot.number] + [DB_TREE[key](tree) for key in DB_TREE]
                table_data.append(temp)
    return table_data


def _get_logs_table(user):
    table_data = [['Stand Name', 'Plot Number', 'Tree Number'] + list(DB_LOG.keys())]
    for stand in user.stands:
        for plot in stand.plots:
            for tree in plot.trees:
                for log in tree.logs:
                    temp = [stand.name, plot.number, tree.number] + [DB_LOG[key](log) for key in DB_LOG]
                    table_data.append(temp)
    return table_data


DB_TABLE_FUNCS = {
    'stands': lambda user: _get_stands_table(user),
    'plots': lambda user: _get_plots_table(user),
    'trees': lambda user: _get_trees_table(user),
    'logs': lambda user: _get_logs_table(user)
}


TABLE_HEADS = ['Species', 'TPA', 'BA/AC', 'RD/AC', 'QMD', 'VBAR', 'AVG HGT', 'HDR', 'BF/AC', 'CF/AC']

METRICS = ['tpa', 'ba_ac', 'rd_ac', 'qmd', 'vbar', 'avg_height', 'hdr', 'bf_ac', 'cf_ac']

SUMMARY_SUMS_PLOT = ['tpa', 'ba_ac', 'rd_ac', 'bf_ac', 'cf_ac']

SUMMARY_CALC_PLOT = {
    'qmd': lambda x: ((x['ba_ac'] / x['tpa']) / .005454) ** 0.5,
    'vbar': lambda x: x['bf_ac'] / x['ba_ac'],
    'avg_height': lambda x: sum(x['avg_height']) / len(x['avg_height']),
    'hdr': lambda x: sum(x['hdr']) / len(x['hdr'])
}

ATTR_TABLES = {
    'Stand': {
        'Name': lambda stand: {'input': True, 'type': 'text', 'val': stand.name},
        'Acres': lambda stand: {'input': True, 'type': 'text', 'val': stand.acres},
        'Plots': lambda stand: {'input': False, 'type': 'text', 'val': len(list(stand.plots))},
        'Trees': lambda stand: {'input': False, 'type': 'text', 'val': sum([len(list(plot.trees)) for plot in stand.plots])},
        'Inventory Date': lambda stand: {'input': True, 'type': 'date', 'val': h_date(stand.date_inventory)},
        'Preferred Log Length': lambda stand: {'input': True, 'type': 'text', 'val': stand.pref_log_length},
        'Minimum Log Length': lambda stand: {'input': True, 'type': 'text', 'val': stand.min_log_length},
        'Utility Log DIB': lambda stand: {'input': True, 'type': 'text', 'val': stand.util_log_dib},
    },
    'Plot': {
        'Plot Number': lambda plot: {'input': False, 'type': 'text', 'val': plot.number},
        'Plot Factor': lambda plot: {'input': True, 'type': 'text', 'val': plot.plot_factor},
        'Trees': lambda plot: {'input': False, 'type': 'text', 'val': plot.tree_count},
    },
    'Tree': {
        'Tree Number': lambda tree: {'input': False, 'type': 'text', 'val': tree.number},
        'Species': lambda tree: {'input': False, 'type': 'text', 'val':  tree.species},
        'DBH': lambda tree: {'input': False, 'type': 'text', 'val':  tree.dbh},
        'Total Height': lambda tree: {'input': False, 'type': 'text', 'val':  f_round_or_blank(tree.total_height)},
        'HDR': lambda tree: {'input': False, 'type': 'text', 'val':  f_round_or_blank(tree.hdr)},
        'BA': lambda tree: {'input': False, 'type': 'text', 'val':  round(tree.ba, 2)},
        'RD': lambda tree: {'input': False, 'type': 'text',  'val': round(tree.rd, 2)},
        'TPA': lambda tree: {'input': False, 'type': 'text', 'val':  f_round_or_blank(tree.tpa)},
        'BA/AC': lambda tree: {'input': False, 'type': 'text', 'val':  f_round_or_blank(tree.ba_ac)},
        'RD/AC': lambda tree: {'input': False, 'type': 'text', 'val':  f_round_or_blank(tree.rd_ac)},
        'Merch DIB': lambda tree: {'input': False, 'type': 'text', 'val':  tree.merch_dib},
        'Merch Height': lambda tree: {'input': False, 'type': 'text', 'val':  tree.merch_height},
        'BF': lambda tree: {'input': False, 'type': 'text', 'val':  f_round_or_blank(tree.bf)},
        'CF': lambda tree: {'input': False, 'type': 'text', 'val':  f_round_or_blank(tree.cf)},
        'BF/AC': lambda tree: {'input': False, 'type': 'text', 'val':  f_round_or_blank(tree.bf_ac)},
        'CF/AC': lambda tree: {'input': False, 'type': 'text', 'val':  f_round_or_blank(tree.cf_ac)},
        'VBAR': lambda tree: {'input': False, 'type': 'text', 'val':  f_round_or_blank(tree.vbar)}
    },
    'Log': {
        'Log Number': lambda log: {'input': False, 'type': 'text', 'val': log.number},
        'Stem Height': lambda log: {'input': False, 'type': 'text', 'val': log.stem_height},
        'Length': lambda log: {'input': False, 'type': 'text', 'val': log.length},
        'Defect': lambda log: {'input': False, 'type': 'text', 'val': log.defect},
        'Species': lambda log: {'input': False, 'type': 'text', 'val': log.species},
        'Logs/AC': lambda log: {'input': False, 'type': 'text', 'val': f_round_or_blank(log.lpa)},
        'Top DIB': lambda log: {'input': False, 'type': 'text', 'val': log.top_dib},
        'Grade': lambda log: {'input': False, 'type': 'text', 'val': log.grade},
        'Grade Name': lambda log: {'input': False, 'type': 'text', 'val': log.grade_name},
        'BF': lambda log: {'input': False, 'type': 'text', 'val': f_round_or_blank(log.bf)},
        'CF': lambda log: {'input': False, 'type': 'text', 'val': f_round_or_blank(log.cf)},
        'BF/AC': lambda log: {'input': False, 'type': 'text', 'val': f_round_or_blank(log.bf_ac)},
        'CF/AC': lambda log: {'input': False, 'type': 'text', 'val': f_round_or_blank(log.cf_ac)}
    }
}


def summary_table_plot(plot):
    summary = {}
    if len(list(plot.trees)) == 0:
        return summary
    else:
        append_lists = ['avg_height', 'hdr']
        totals = {
            'tpa': 0,
            'ba_ac': 0,
            'rd_ac': 0,
            'qmd': 0,
            'vbar': 0,
            'avg_height': [],
            'hdr': [],
            'bf_ac': 0,
            'cf_ac': 0
        }
        for tree in plot.trees:
            if tree.species not in summary:
                summary[tree.species] = {}
                for key in totals:
                    if key in append_lists:
                        summary[tree.species][key] = []
                    else:
                        summary[tree.species][key] = 0
            for key in totals:
                if key in SUMMARY_SUMS_PLOT:
                    val = getattr(tree, key)
                    summary[tree.species][key] += val
                    totals[key] += val
                elif key in append_lists:
                    if key == 'hdr':
                        val = getattr(tree, key)
                        summary[tree.species][key].append(val)
                        totals[key].append(val)
                    else:
                        val = getattr(tree, 'total_height')
                        summary[tree.species][key].append(val)
                        totals[key].append(val)
        summary['totals'] = totals
        for spp in summary:
            for key in SUMMARY_CALC_PLOT:
                summary[spp][key] = SUMMARY_CALC_PLOT[key](summary[spp])
        return summary


def summary_table_stand(stand):
    summary = {}
    for plot in stand.plots:
        plot_summary = summary_table_plot(plot)
        if plot_summary:
            for spp in plot_summary:
                if spp not in summary:
                    summary[spp] = {key: [] for key in METRICS}
                for key in METRICS:
                    if key not in ['qmd', 'vbar']:
                        summary[spp][key].append(plot_summary[spp][key])
    for spp in summary:
        for key in SUMMARY_SUMS_PLOT:
            summary[spp][key] = sum(summary[spp][key]) / len(list(stand.plots))
    for spp in summary:
        for key in SUMMARY_CALC_PLOT:
            summary[spp][key] = SUMMARY_CALC_PLOT[key](summary[spp])

    # FOR SORTING - PUT TOTALS AT BOTTOM OF DICT
    hold = (summary['totals'], )
    del summary['totals']
    summary['totals'] = hold[0]
    return summary


SUMMARY_FUNCS = {
    'Stand': lambda stand: summary_table_stand(stand),
    'Plot': lambda plot: summary_table_plot(plot)
}



















