"""update organization

Revision ID: acd71a81df34
Revises: 6fa9f13d06fa
Create Date: 2025-04-25 00:53:30.366933

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'acd71a81df34'
down_revision: Union[str, None] = '6fa9f13d06fa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('organization', sa.Column('created_vacancy_at', sa.String(), nullable=True))
    op.add_column('organization', sa.Column('updated_vacancy_at', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('organization', 'updated_vacancy_at')
    op.drop_column('organization', 'created_vacancy_at')
    # ### end Alembic commands ###
