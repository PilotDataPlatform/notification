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

from pydantic import BaseModel

from app.models.base_models import APIResponse


class POSTEmail(BaseModel):
    sender: str
    receiver: list
    subject: str = ''
    message: str = ''
    template: str = ''
    template_kwargs: dict = {}
    msg_type: str = 'plain'
    attachments: list = []


class POSTEmailResponse(APIResponse):
    result: str = 'success'
