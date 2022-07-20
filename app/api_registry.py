# Copyright (C) 2022 Indoc Research
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from fastapi import FastAPI
from fastapi_health import health

from .routers.v1.api_announcement import api_announcement
from .routers.v1.api_email import api_email
from .routers.v1.api_notification import api_notification
from .routers.v1.health.api_health import opsdb_check


def api_registry(app: FastAPI):
    app.add_api_route(
        '/v1/health/',
        health([opsdb_check],
        success_status=204),
        tags=['Health'])
    app.include_router(
        api_announcement.router,
        prefix='/v1/announcements',
        tags=['announcement'])
    app.include_router(
        api_email.router,
        prefix='/v1/email',
        tags=['email'])
    app.include_router(
        api_notification.router,
        prefix='/v1/notification',
        tags=['notification'])
    app.include_router(
        api_notification.routerBulk,
        prefix='/v1/notifications',
        tags=['notification'])
    app.include_router(
        api_notification.routerUnsub,
        prefix='/v1/unsubscribe',
        tags=['notification'])
