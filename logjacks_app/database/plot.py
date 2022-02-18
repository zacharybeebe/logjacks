from logjacks_app.database.db import db, orm
from logjacks_app.database.tables import stand_plots


class Plot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    stand_id = db.Column(db.Integer, db.ForeignKey('stand.id'), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    plot_factor = db.Column(db.Float, nullable=False)
    plots = db.relationship('Stand', secondary=stand_plots, backref=db.backref('plots', lazy=True))

    @orm.reconstructor
    def init_on_load(self, **kwargs):
        super(Plot, self).__init__(**kwargs)
        self.tree_count = len(list(self.trees))

        if self.tree_count > 0:
            self.tpa = sum([tree.tpa for tree in self.trees])
            self.ba_ac = sum([tree.ba_ac for tree in self.trees])
            self.qmd = ((self.ba_ac / self.tpa) / .005454) ** 0.5
            self.rd_ac = sum([tree.rd_ac for tree in self.trees])
            self.bf_ac = sum([tree.bf_ac for tree in self.trees])
            self.cf_ac = sum([tree.cf_ac for tree in self.trees])
            self.avg_hgt = sum([tree.total_height for tree in self.trees]) / self.tree_count
            self.vbar = self.bf_ac / self.ba_ac
        else:
            self.tpa = 0
            self.ba_ac = 0
            self.qmd = 0
            self.rd_ac = 0
            self.bf_ac = 0
            self.cf_ac = 0
            self.avg_hgt = 0
            self.vbar = 0
