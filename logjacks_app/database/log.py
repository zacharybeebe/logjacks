from logjacks_app.database.db import db, orm
from logjacks_app.database.tables import tree_logs


class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
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

    @orm.reconstructor
    def init_on_load(self, **kwargs):
        super(Log, self).__init__(**kwargs)
