"""Edit notification permissions

Revision ID: 18229713a828
Revises: 6aeab8bf0e11
Create Date: 2022-01-19 13:48:26.837465

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '18229713a828'
down_revision = '6aeab8bf0e11'
branch_labels = None
depends_on = None

def upgrade():
    op.execute("INSERT INTO public.casbin_rule(v0, v1, v2, v3, ptype) VALUES('platform_admin', '*', 'notification', 'view', 'p')")
    # platform_admin notification create already exists
    op.execute("INSERT INTO public.casbin_rule(v0, v1, v2, v3, ptype) VALUES('platform_admin', '*', 'notification', 'update', 'p')")
    op.execute("INSERT INTO public.casbin_rule(v0, v1, v2, v3, ptype) VALUES('platform_admin', '*', 'notification', 'delete', 'p')")
    op.execute("INSERT INTO public.casbin_rule(v0, v1, v2, v3, ptype) VALUES('admin', '*', 'notification', 'view', 'p')")
    op.execute("INSERT INTO public.casbin_rule(v0, v1, v2, v3, ptype) VALUES('contributor', '*', 'notification', 'view', 'p')")
    op.execute("INSERT INTO public.casbin_rule(v0, v1, v2, v3, ptype) VALUES('collaborator', '*', 'notification', 'view', 'p')")
    op.execute("INSERT INTO public.casbin_rule(v0, v1, v2, v3, ptype) VALUES('member', '*', 'notification', 'view', 'p')")
    op.execute("INSERT INTO public.casbin_rule(v0, v1, v2, v3, ptype) VALUES('visitor', '*', 'notification', 'view', 'p')")
    op.execute("INSERT INTO public.casbin_rule(v0, v1, v2, v3, ptype) VALUES('platform_admin', '*', 'email', 'create', 'p')")

def downgrade():
    op.execute("DELETE FROM public.casbin_rule WHERE v0='platform_admin' AND v1='*' AND v2='notification' AND v3='view'")
    op.execute("DELETE FROM public.casbin_rule WHERE v0='platform_admin' AND v1='*' AND v2='notification' AND v3='update'")
    op.execute("DELETE FROM public.casbin_rule WHERE v0='platform_admin' AND v1='*' AND v2='notification' AND v3='delete'")
    op.execute("DELETE FROM public.casbin_rule WHERE v0='admin' AND v1='*' AND v2='notification' AND v3='view'")
    op.execute("DELETE FROM public.casbin_rule WHERE v0='contributor' AND v1='*' AND v2='notification' AND v3='view'")
    op.execute("DELETE FROM public.casbin_rule WHERE v0='collaborator' AND v1='*' AND v2='notification' AND v3='view'")
    op.execute("DELETE FROM public.casbin_rule WHERE v0='member' AND v1='*' AND v2='notification' AND v3='view'")
    op.execute("DELETE FROM public.casbin_rule WHERE v0='visitor' AND v1='*' AND v2='notification' AND v3='view'")
    op.execute("DELETE FROM public.casbin_rule WHERE v0='platform_admin' AND v1='*' AND v2='notification' AND v3='create'")
