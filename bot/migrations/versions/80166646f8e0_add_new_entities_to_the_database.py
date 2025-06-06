"""add new entities to the database

Revision ID: 80166646f8e0
Revises: eace85a6fe8f
Create Date: 2025-04-23 19:34:55.650645

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '80166646f8e0'
down_revision: Union[str, None] = 'eace85a6fe8f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('address',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('competency',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('education_level',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('educational_type',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('employment_type',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('experience',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('schedule',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('organization',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('parent_id', sa.BigInteger(), nullable=True),
    sa.Column('educational_type_id', sa.BigInteger(), nullable=True),
    sa.Column('full_title', sa.String(), nullable=True),
    sa.Column('full_title_eng', sa.String(), nullable=True),
    sa.Column('short_title', sa.String(), nullable=True),
    sa.Column('short_title_eng', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('description_eng', sa.String(), nullable=True),
    sa.Column('supervisor_fio', sa.String(), nullable=True),
    sa.Column('supervisor_fio_eng', sa.String(), nullable=True),
    sa.Column('supervisor_job_title', sa.String(), nullable=True),
    sa.Column('supervisor_job_title_eng', sa.String(), nullable=True),
    sa.Column('status', sa.Boolean(), nullable=True),
    sa.Column('is_participant', sa.Boolean(), nullable=True),
    sa.Column('is_published', sa.Boolean(), nullable=True),
    sa.Column('inn', sa.String(), nullable=True),
    sa.Column('ogrn', sa.String(), nullable=True),
    sa.Column('address', sa.String(), nullable=True),
    sa.Column('address_eng', sa.String(), nullable=True),
    sa.Column('phone', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('vk', sa.String(), nullable=True),
    sa.Column('telegram', sa.String(), nullable=True),
    sa.Column('site', sa.String(), nullable=True),
    sa.Column('is_educational', sa.Boolean(), nullable=True),
    sa.Column('is_head', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['educational_type_id'], ['educational_type.id'], ),
    sa.ForeignKeyConstraint(['parent_id'], ['organization.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('attachment',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('url', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('organization_logo_id', sa.BigInteger(), nullable=True),
    sa.Column('organization_licenze_id', sa.BigInteger(), nullable=True),
    sa.Column('organization_accreditation_id', sa.BigInteger(), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['organization_accreditation_id'], ['organization.id'], ),
    sa.ForeignKeyConstraint(['organization_licenze_id'], ['organization.id'], ),
    sa.ForeignKeyConstraint(['organization_logo_id'], ['organization.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('vacancy',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('salary_from', sa.Integer(), nullable=True),
    sa.Column('salary_up_to', sa.Integer(), nullable=True),
    sa.Column('before_tax', sa.Boolean(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('contact_name', sa.String(), nullable=True),
    sa.Column('phone', sa.String(), nullable=True),
    sa.Column('is_blocked', sa.Boolean(), nullable=False),
    sa.Column('published_at', sa.String(), nullable=False),
    sa.Column('is_favorite', sa.Boolean(), nullable=False),
    sa.Column('hh_url', sa.String(), nullable=True),
    sa.Column('organization_id', sa.BigInteger(), nullable=False),
    sa.Column('employment_type_id', sa.BigInteger(), nullable=True),
    sa.Column('experience_id', sa.BigInteger(), nullable=True),
    sa.Column('education_level_id', sa.BigInteger(), nullable=True),
    sa.Column('address_id', sa.BigInteger(), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['address_id'], ['address.id'], ),
    sa.ForeignKeyConstraint(['education_level_id'], ['education_level.id'], ),
    sa.ForeignKeyConstraint(['employment_type_id'], ['employment_type.id'], ),
    sa.ForeignKeyConstraint(['experience_id'], ['experience.id'], ),
    sa.ForeignKeyConstraint(['organization_id'], ['organization.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('vacancy_desirable_competency',
    sa.Column('vacancy_id', sa.BigInteger(), nullable=False),
    sa.Column('competency_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['competency_id'], ['competency.id'], ),
    sa.ForeignKeyConstraint(['vacancy_id'], ['vacancy.id'], ),
    sa.PrimaryKeyConstraint('vacancy_id', 'competency_id')
    )
    op.create_table('vacancy_main_competency',
    sa.Column('vacancy_id', sa.BigInteger(), nullable=False),
    sa.Column('competency_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['competency_id'], ['competency.id'], ),
    sa.ForeignKeyConstraint(['vacancy_id'], ['vacancy.id'], ),
    sa.PrimaryKeyConstraint('vacancy_id', 'competency_id')
    )
    op.create_table('vacancy_schedule',
    sa.Column('vacancy_id', sa.BigInteger(), nullable=False),
    sa.Column('schedule_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['schedule_id'], ['schedule.id'], ),
    sa.ForeignKeyConstraint(['vacancy_id'], ['vacancy.id'], ),
    sa.PrimaryKeyConstraint('vacancy_id', 'schedule_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('vacancy_schedule')
    op.drop_table('vacancy_main_competency')
    op.drop_table('vacancy_desirable_competency')
    op.drop_table('vacancy')
    op.drop_table('attachment')
    op.drop_table('organization')
    op.drop_table('schedule')
    op.drop_table('experience')
    op.drop_table('employment_type')
    op.drop_table('educational_type')
    op.drop_table('education_level')
    op.drop_table('competency')
    op.drop_table('address')
    # ### end Alembic commands ###
