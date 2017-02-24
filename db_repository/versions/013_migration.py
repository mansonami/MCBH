from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
user = Table('user', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('email', VARCHAR(length=64)),
    Column('password', VARCHAR(length=126)),
    Column('username', VARCHAR(length=64)),
    Column('Wx_uid', VARCHAR(length=126)),
    Column('emarkName', VARCHAR(length=64)),
    Column('nickName', VARCHAR(length=64)),
    Column('right', INTEGER),
    Column('wx_uin', VARCHAR(length=126)),
)

user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('email', String(length=64)),
    Column('username', String(length=64)),
    Column('password', String(length=126)),
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
    pre_meta.tables['user'].columns['Wx_uid'].drop()
    pre_meta.tables['user'].columns['emarkName'].drop()
    pre_meta.tables['user'].columns['nickName'].drop()
    post_meta.tables['user'].columns['nickname'].create()
    post_meta.tables['user'].columns['remarkname'].create()
    post_meta.tables['user'].columns['wx_uid'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['user'].columns['Wx_uid'].create()
    pre_meta.tables['user'].columns['emarkName'].create()
    pre_meta.tables['user'].columns['nickName'].create()
    post_meta.tables['user'].columns['nickname'].drop()
    post_meta.tables['user'].columns['remarkname'].drop()
    post_meta.tables['user'].columns['wx_uid'].drop()
