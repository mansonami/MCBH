from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
wx_user = Table('wx_user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('wx_uin', String(length=126)),
    Column('wx_uid', String(length=126)),
    Column('nickname', String(length=64)),
    Column('remarkname', String(length=64)),
    Column('right', Integer, default=ColumnDefault(1)),
)

user = Table('user', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('email', VARCHAR(length=64)),
    Column('password', VARCHAR(length=126)),
    Column('username', VARCHAR(length=64)),
    Column('right', INTEGER),
    Column('wx_uin', VARCHAR(length=126)),
    Column('nickname', VARCHAR(length=64)),
    Column('remarkname', VARCHAR(length=64)),
    Column('wx_uid', VARCHAR(length=126)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['wx_user'].create()
    pre_meta.tables['user'].columns['nickname'].drop()
    pre_meta.tables['user'].columns['remarkname'].drop()
    pre_meta.tables['user'].columns['right'].drop()
    pre_meta.tables['user'].columns['wx_uid'].drop()
    pre_meta.tables['user'].columns['wx_uin'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['wx_user'].drop()
    pre_meta.tables['user'].columns['nickname'].create()
    pre_meta.tables['user'].columns['remarkname'].create()
    pre_meta.tables['user'].columns['right'].create()
    pre_meta.tables['user'].columns['wx_uid'].create()
    pre_meta.tables['user'].columns['wx_uin'].create()
