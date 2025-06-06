"""Remove uniqueness

Revision ID: 8a973b374193
Revises: cde85cb21a27
Create Date: 2025-04-18 23:36:17.607783

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8a973b374193'
down_revision: Union[str, None] = 'cde85cb21a27'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('memeberstatuss_member_status_name_key', 'memeberstatuss', type_='unique')
    op.drop_constraint('organizerphones_phone_number_key', 'organizerphones', type_='unique')
    op.drop_constraint('periods_lower_key', 'periods', type_='unique')
    op.drop_constraint('periods_upper_key', 'periods', type_='unique')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('periods_upper_key', 'periods', ['upper'])
    op.create_unique_constraint('periods_lower_key', 'periods', ['lower'])
    op.create_unique_constraint('organizerphones_phone_number_key', 'organizerphones', ['phone_number'])
    op.create_unique_constraint('memeberstatuss_member_status_name_key', 'memeberstatuss', ['member_status_name'])
    # ### end Alembic commands ###
