from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
wxsetting = Table('wxsetting', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('adminphone', String(length=64)),
    Column('OnSendalarmMsg', Boolean),
    Column('Reboton', Boolean),
    Column('Add_friend', Boolean),
    Column('Get_vip_integral', Boolean),
    Column('Send_bill_balance_teble', Boolean),
    Column('Sale_table', Boolean),
    Column('Sale_today', Boolean),
    Column('Sale_Brand_All', Boolean),
    Column('Sale_Brand_Table', Boolean),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['wxsetting'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['wxsetting'].drop()
