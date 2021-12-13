from faker import Faker
from logjacks_app.fake_data.fake_tree_data import get_timber, randint, choice, randrange

f = Faker()


def test_user():
    kwargs = {
        'f_name': 'Zach',
        'l_name': 'Beebe',
        'email': 'zach.beebe@logjacks.com',
        'phone': '425-931-8214',
        'company': 'LogJacks',
        'username': 'zach',
        'password': 'zach'
    }
    return kwargs


def fake_user():
    f_name = f.unique.first_name()
    l_name = f.unique.last_name()
    kwargs = {
        'f_name': f_name,
        'l_name': l_name,
        'email': f'{f_name}.{l_name}@fake.com',
        'phone': f.phone_number(),
        'company': f.company(),
        'username': f.unique.user_name(),
        'password': f.password()
    }
    print(kwargs['username'], kwargs['password'])
    return kwargs


def fake_stand():
    kwargs = {
        'name': ''.join([chr(choice([randrange(48, 57), randrange(65, 70)])) for _ in range(8)]),
        'acres': randrange(10, 100),
        'pref_log_length': choice([40, 38, 36, 34, 32]),
        'min_log_length': choice([16, 14, 12, 10, 8]),
        'util_log_dib': 3
    }
    return kwargs


def fake_plot(number, plot_factor):
    kwargs = {
        'number': number,
        'plot_factor': plot_factor
    }
    return kwargs


def fake_tree(locale, age, plot_factor, number, quick=True):
    tree = get_timber(locale, age, plot_factor, quick)
    kwargs = {
        'number': number,
        'plot_factor': plot_factor,
        'species': tree.species,
        'dbh': tree.dbh,
        'total_height': tree.total_height,
        'hdr': tree.hdr,
        'ba': tree.ba,
        'rd': tree.rd,
        'tpa': tree.tpa,
        'ba_ac': tree.ba_ac,
        'rd_ac': tree.rd_ac,
        'stem_dibs': tree.stem_dibs,
        'dib_heights': tree.dib_heights,
        'merch_dib': tree.merch_dib,
        'merch_height': tree.merch_height,
        'bf': tree.bf,
        'cf': tree.cf,
        'bf_ac': tree.bf_ac,
        'cf_ac': tree.cf_ac,
        'vbar': tree.vbar
    }
    logs = [fake_log(key, tree.logs[key]) for key in tree.logs]
    return kwargs, logs


def fake_log(number, log):
    kwargs = {
        'number': number,
        'stem_height': log.stem_height,
        'length': log.length,
        'defect': log.defect,
        'species': log.species,
        'lpa': log.lpa,
        'top_dib': log.top_dib,
        'grade': log.grade,
        'grade_name': log.grade_name,
        'scrib': log.scrib,
        'bf': log.bf,
        'cf': log.cf,
        'bf_ac': log.bf_ac,
        'cf_ac': log.cf_ac,
    }
    return kwargs


def populate_fake_stand(db, User, Stand, Plot, Tree, Log, locale, age, plot_factor, user_type='fake', stands=1, plots=20, quick=True):
    if user_type == 'fake':
        user_kwargs = fake_user()
        user = User(**user_kwargs)
    else:
        user_kwargs = test_user()
        user = User(**user_kwargs)
    db.session.add(user)
    db.session.commit()

    for s in range(stands):
        stand_kwargs = fake_stand()
        stand_kwargs['user_id'] = user.id
        stand = Stand(**stand_kwargs)
        db.session.add(stand)
        db.session.commit()

        for p in range(1, plots + 1):
            plot_kwargs = fake_plot(p, plot_factor)
            plot = Plot(user_id=user.id, stand_id=stand.id, **plot_kwargs)
            db.session.add(plot)
            db.session.commit()

            trees = randint(0, 10)
            if trees > 0:
                for i in range(1, trees + 1):
                    tree_kwargs, logs = fake_tree(locale, age, plot_factor, i, quick=quick)
                    tree = Tree(user_id=user.id, stand_id=stand.id, plot_id=plot.id, **tree_kwargs)
                    db.session.add(tree)
                    db.session.commit()
                    for log_kwargs in logs:
                        log = Log(user_id=user.id, stand_id=stand.id, plot_id=plot.id, tree_id=tree.id, **log_kwargs)
                        db.session.add(log)
                        db.session.commit()
                        tree.logs.append(log)
                    plot.trees.append(tree)
            stand.plots.append(plot)
        user.stands.append(stand)
    db.session.commit()
