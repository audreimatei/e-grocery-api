from typing import TypeVar

from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    metadata = MetaData(
        naming_convention={
            'all_column_names': lambda constraint, table: '_'.join(  # type: ignore
                [column.name for column in constraint.columns.values()]
            ),
            'ix': 'ix__%(all_column_names)s',
            'uq': 'uq__%(table_name)s__%(all_column_names)s',
            'ck': 'ck__%(table_name)s__%(constraint_name)s',
            'fk': (
                'fk__%(table_name)s__'
                '%(all_column_names)s__'
                '%(referred_table_name)s'
            ),
            'pk': 'pk__%(table_name)s'
        }
    )

    def __repr__(self):
        fields = ', '.join(
            f'{key}={value}'
            for key, value in self.__dict__.items()
            if not key.startswith('_')
        )
        return f'<{self.__class__.__name__}=({fields})>'


ModelType = TypeVar('ModelType', bound=Base)
