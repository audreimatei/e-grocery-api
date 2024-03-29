"""empty message

Revision ID: 7d79737c9cb3
Revises: 
Create Date: 2023-08-23 18:30:07.948434

"""
from alembic import op
import geoalchemy2
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '7d79737c9cb3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('couriers',
    sa.Column('courier_id', sa.Uuid(), nullable=False),
    sa.Column('courier_type', sa.Enum('FOOT', 'BIKE', 'AUTO', name='couriertype'), nullable=False),
    sa.PrimaryKeyConstraint('courier_id', name=op.f('pk__couriers'))
    )
    op.create_table('items',
    sa.Column('item_id', sa.Uuid(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('weight', sa.Integer(), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('item_id', name=op.f('pk__items')),
    sa.UniqueConstraint('name', name=op.f('uq__items__name'))
    )
    op.create_table('regions',
    sa.Column('region_id', sa.Uuid(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('_geo_polygon', geoalchemy2.types.Geography(geometry_type='POLYGON', srid=4326, from_text='ST_GeogFromText', name='geography', nullable=False), nullable=False),
    sa.PrimaryKeyConstraint('region_id', name=op.f('pk__regions'))
    )
    op.create_table('orders',
    sa.Column('order_id', sa.Uuid(), nullable=False),
    sa.Column('courier_id', sa.Uuid(), nullable=True),
    sa.Column('delivery_region_id', sa.Uuid(), nullable=False),
    sa.Column('delivery_address', sa.String(), nullable=False),
    sa.Column('_delivery_location', geoalchemy2.types.Geography(geometry_type='POINT', srid=4326, from_text='ST_GeogFromText', name='geography', nullable=False), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('completed_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['courier_id'], ['couriers.courier_id'], name=op.f('fk__orders__courier_id__couriers')),
    sa.ForeignKeyConstraint(['delivery_region_id'], ['regions.region_id'], name=op.f('fk__orders__delivery_region_id__regions')),
    sa.PrimaryKeyConstraint('order_id', name=op.f('pk__orders'))
    )
    op.create_table('shifts',
    sa.Column('shift_id', sa.Uuid(), nullable=False),
    sa.Column('region_id', sa.Uuid(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('start_time', sa.Time(), nullable=False),
    sa.Column('end_time', sa.Time(), nullable=False),
    sa.ForeignKeyConstraint(['region_id'], ['regions.region_id'], name=op.f('fk__shifts__region_id__regions')),
    sa.PrimaryKeyConstraint('shift_id', name=op.f('pk__shifts'))
    )
    op.create_table('couriers_shifts',
    sa.Column('courier_id', sa.Uuid(), nullable=False),
    sa.Column('shift_id', sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(['courier_id'], ['couriers.courier_id'], name=op.f('fk__couriers_shifts__courier_id__couriers')),
    sa.ForeignKeyConstraint(['shift_id'], ['shifts.shift_id'], name=op.f('fk__couriers_shifts__shift_id__shifts')),
    sa.PrimaryKeyConstraint('courier_id', 'shift_id', name=op.f('pk__couriers_shifts'))
    )
    op.create_table('orders_items',
    sa.Column('order_id', sa.Uuid(), nullable=False),
    sa.Column('item_id', sa.Uuid(), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['item_id'], ['items.item_id'], name=op.f('fk__orders_items__item_id__items')),
    sa.ForeignKeyConstraint(['order_id'], ['orders.order_id'], name=op.f('fk__orders_items__order_id__orders')),
    sa.PrimaryKeyConstraint('order_id', 'item_id', name=op.f('pk__orders_items'))
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('orders_items')
    op.drop_table('couriers_shifts')
    op.drop_table('shifts')
    op.drop_table('orders')
    op.drop_table('regions')
    op.drop_table('items')
    op.drop_table('couriers')
    # ### end Alembic commands ###
