from logjacks_app.database.db import db, orm, datetime, timezone
from logjacks_app.database.datatypes import UTCDateTime
from logjacks_app.database.tables import user_stands


class Stand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(128), nullable=False)
    acres = db.Column(db.Float)
    date_inventory = db.Column(UTCDateTime(timezone=True), nullable=False, default=datetime.now(timezone.utc))
    stands = db.relationship('User', secondary=user_stands, backref=db.backref('stands', lazy=True))

    @orm.reconstructor
    def init_on_load(self, **kwargs):
        super(Stand, self).__init__(**kwargs)
        self.plot_count = len(list(self.plots))
        self.tree_count = sum([len(list(plot.trees)) for plot in self.plots])

        if self.plot_count > 0:
            self.tpa = sum([plot.tpa for plot in self.plots]) / self.plot_count
            self.ba_ac = sum([plot.ba_ac for plot in self.plots]) / self.plot_count
            self.qmd = ((self.ba_ac / self.tpa) / .005454) ** 0.5
            self.rd_ac = sum([plot.rd_ac for plot in self.plots]) / self.plot_count
            self.bf_ac = sum([plot.bf_ac for plot in self.plots]) / self.plot_count
            self.cf_ac = sum([plot.cf_ac for plot in self.plots]) / self.plot_count
            self.avg_hgt = sum([plot.avg_hgt for plot in self.plots]) / self.plot_count
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
