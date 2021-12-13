from datetime import datetime
from flask_sqlalchemy import SQLAlchemy, orm
from logjacks_app import app
from logjacks_app.database.models_custom_types import *

db = SQLAlchemy(app)

user_stands = db.Table(
	'user_stands',
	db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
	db.Column('stand_id', db.Integer, db.ForeignKey('stand.id'), primary_key=True)
)

stand_plots = db.Table(
	'stand_plots',
	db.Column('stand_id', db.Integer, db.ForeignKey('stand.id'), primary_key=True),
	db.Column('plot_id', db.Integer, db.ForeignKey('plot.id'), primary_key=True)
)

plot_trees = db.Table(
	'plot_trees',
	db.Column('plot_id', db.Integer, db.ForeignKey('plot.id'), primary_key=True),
	db.Column('tree_id', db.Integer, db.ForeignKey('tree.id'), primary_key=True)
)

tree_logs = db.Table(
	'tree_logs',
	db.Column('tree_id', db.Integer, db.ForeignKey('tree.id'), primary_key=True),
	db.Column('log_id', db.Integer, db.ForeignKey('log.id'), primary_key=True)
)


class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date_created = db.Column(UTCDateTime(timezone=True), nullable=False, default=datetime.now(timezone.utc))
	f_name = db.Column(db.String(128), nullable=False)
	l_name = db.Column(db.String(128), nullable=False)
	email = db.Column(db.String(128), nullable=False, unique=True)
	phone = db.Column(db.String(32), nullable=True)
	company = db.Column(db.String(128), nullable=True)
	username = db.Column(db.String(128), nullable=False, unique=True)
	password = db.Column(Sensitive, nullable=False)


class Stand(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	name = db.Column(db.String(128), nullable=False)
	acres = db.Column(db.Float, nullable=True)
	date_inventory = db.Column(UTCDateTime(timezone=True), nullable=False, default=datetime.now(timezone.utc))
	pref_log_length = db.Column(db.Integer, nullable=False, default=40)
	min_log_length = db.Column(db.Integer, nullable=False, default=16)
	util_log_dib = db.Column(db.Integer, nullable=False, default=3)
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


class Plot(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	stand_id = db.Column(db.Integer, db.ForeignKey('stand.id'), nullable=False)
	number = db.Column(db.Integer)
	plot_factor = db.Column(db.Float)
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


class Tree(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	stand_id = db.Column(db.Integer, db.ForeignKey('stand.id'), nullable=False)
	plot_id = db.Column(db.Integer, db.ForeignKey('plot.id'), nullable=False)
	number = db.Column(db.Integer)
	plot_factor = db.Column(db.Float)
	species = db.Column(db.String(4))
	dbh = db.Column(db.Float)
	total_height = db.Column(db.Float)

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


class Log(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	stand_id = db.Column(db.Integer, db.ForeignKey('stand.id'), nullable=False)
	plot_id = db.Column(db.Integer, db.ForeignKey('plot.id'), nullable=False)
	tree_id = db.Column(db.Integer, db.ForeignKey('tree.id'), nullable=False)

	number = db.Column(db.Integer)
	stem_height = db.Column(db.Integer)
	length = db.Column(db.Integer)
	defect = db.Column(db.Integer)
	species = db.Column(db.String(4))
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
