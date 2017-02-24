from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
wx_post = Table('wx_post', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('sender', VARCHAR(length=126)),
    Column('body', VARCHAR(length=140)),
    Column('timestamp', DATETIME),
    Column('wxuser_id', INTEGER),
)

wx_user = Table('wx_user', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('wx_uin', VARCHAR(length=126)),
    Column('wx_uid', VARCHAR(length=126)),
    Column('nickname', VARCHAR(length=64)),
    Column('remarkname', VARCHAR(length=64)),
    Column('right', INTEGER),
)

wxpost = Table('wxpost', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('sender', String(length=126)),
    Column('body', String(length=140)),
    Column('timestamp', DateTime),
    Column('wxuser_id', Integer),
)

wxuser = Table('wxuser', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('wx_uin', String(length=126)),
    Column('wx_uid', String(length=126)),
    Column('nickname', String(length=64)),
    Column('remarkname', String(length=64)),
    Column('right', Integer, default=ColumnDefault(1)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['wx_post'].drop()
    pre_meta.tables['wx_user'].drop()
    post_meta.tables['wxpost'].create()
    post_meta.tables['wxuser'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['wx_post'].create()
    pre_meta.tables['wx_user'].create()
    post_meta.tables['wxpost'].drop()
    post_meta.tables['wxuser'].drop()
