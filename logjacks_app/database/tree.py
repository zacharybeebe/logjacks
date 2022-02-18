from logjacks_app.database.db import db, orm
from logjacks_app.database.datatypes import Blob
from logjacks_app.database.tables import plot_trees


class Tree(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    stand_id = db.Column(db.Integer, db.ForeignKey('stand.id'), nullable=False)
    plot_id = db.Column(db.Integer, db.ForeignKey('plot.id'), nullable=False)
    plot_factor = db.Column(db.Float, db.ForeignKey('plot.plot_factor'), nullable=False)
    number = db.Column(db.Integer, nullable=False)

    species = db.Column(db.String(4), nullable=False)
    dbh = db.Column(db.Float, nullable=False)
    total_height = db.Column(db.Float, nullable=False)

    hdr = db.Column(db.Float)
    ba = db.Column(db.Float)
    rd = db.Column(db.Float)
    tpa = db.Column(db.Float)
    ba_ac = db.Column(db.Float)
    rd_ac = db.Column(db.Float)
    stem_dibs = db.Column(Blob)
    dib_heights = db.Column(Blob)

    merch_dib = db.Column(db.Integer)
    merch_height = db.Column(db.Integer)

    bf = db.Column(db.Float)
    cf = db.Column(db.Float)
    bf_ac = db.Column(db.Float)
    cf_ac = db.Column(db.Float)
    vbar = db.Column(db.Float)

    trees = db.relationship('Plot', secondary=plot_trees, backref=db.backref('trees', lazy=True))

    @orm.reconstructor
    def init_on_load(self, **kwargs):
        super(Tree, self).__init__(**kwargs)
