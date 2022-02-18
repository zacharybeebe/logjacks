from logjacks_app.database.db import db

user_stands = db.Table(
    'user_stands',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('stand_id', db.Integer, db.ForeignKey('stand.id'), primary_key=True)
)

# user_inventory = db.Table(
#     'user_inventory',
#     db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
#     db.Column('inventory_id', db.Integer, db.ForeignKey('inventory.id'), primary_key=True)
# )

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
