from logjacks_app.timber.timber import TimberQuick, TimberFull
from logjacks_app.timber.constants import ALL_SPECIES_NAMES
from random import randint, randrange, choice

LOCALES = {
    'coastal wa con': (['DF'] * 40) + (['WH'] * 20) + (['SS'] * 15) + (['RC'] * 15) + (['RA'] * 3) + (['LP'] * 2) + (['BM'] * 2) + (['CW'] * 1),
    'coastal wa hwd': (['RA'] * 40) + (['BM'] * 20) + (['CW'] * 15) + (['DF'] * 15) + (['RC'] * 3) + (['LP'] * 2) + (['WH'] * 2) + (['SS'] * 1),
    'puget wa con': (['DF'] * 50) + (['WH'] * 25) + (['RC'] * 15) + (['RA'] * 3) + (['SS'] * 2) + (['BM'] * 2) + (['CW'] * 1),
    'puget wa hwd': (['RA'] * 40) + (['BM'] * 25) + (['CW'] * 15) + (['DF'] * 15) + (['RC'] * 4) + (['WH'] * 3) + (['SS'] * 1),

}

DEFECT = ([0] * 10) + ([5] * 5) + ([10] * 5) + ([15] * 1)


def _get_dbh_range(age):
    if age in range(20, 30):
        return ([randrange(60, 109)] * 70) + ([randrange(110, 149)] * 30)
    elif age in range(30, 40):
        return ([randrange(60, 109)] * 20) + ([randrange(110, 149)] * 50) + ([randrange(150, 199)] * 30)
    elif age in range(40, 50):
        return ([randrange(60, 109)] * 5) + ([randrange(110, 149)] * 25) + ([randrange(150, 199)] * 50) + ([randrange(199, 269)] * 20)
    else:
        return ([randrange(60, 109)] * 3) + ([randrange(110, 179)] * 7) + ([randrange(180, 249)] * 30) + ([randrange(250, 299)] * 30) + ([randrange(300, 450)] * 20)


def _get_tree_specs(age):
    dbh = choice(_get_dbh_range(age))
    if dbh in range(60, 109):
        hdr = randrange(60, 85)
    elif dbh in range(110, 179):
        hdr = randrange(55, 75)
    elif dbh in range(180, 299):
        hdr = randrange(48, 71)
    else:
        hdr = randrange(40, 62)
    dbh = dbh / 10
    hgt = (dbh / 12) * hdr
    return dbh, hgt


def get_timber(locale, age, plot_factor, quick=True):
    spp = choice(LOCALES[locale])
    dbh, hgt = _get_tree_specs(age)
    tree = TimberQuick(plot_factor, spp, dbh, hgt)
    if quick:
        return tree
    else:
        logs_specs = []
        for l_num in tree.logs:
            log = tree.logs[l_num]
            logs_specs.append([log.stem_height, log.length, choice(DEFECT), log.grade])
        t_full = TimberFull(plot_factor, spp, dbh, hgt)
        for log in logs_specs:
            t_full.add_log(*log)
        return t_full