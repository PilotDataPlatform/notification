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
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

from app.models.base_models import APIResponse


async def paginate(params: BaseModel, api_response: APIResponse, query: select, db: AsyncSession):
    query = query.limit(params.page_size).offset(
        params.page * params.page_size)
    items = (await db.execute(query)).scalars().all()
    total = len(items)
    results = []
    for item in items:
        results.append(item.to_dict())
    api_response.page = params.page
    api_response.num_of_pages = int(int(total) / int(params.page_size))
    api_response.total = total
    api_response.result = results
