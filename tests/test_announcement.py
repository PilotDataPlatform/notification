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

import pytest

pytestmark = pytest.mark.asyncio


class TestAnnouncement:

    async def test_01_post_announcement(self, test_client):
        payload = {
            'project_code': 'test_01',
            'content': 'Content for test announcement',
            'publisher': 'erik'
        }
        response = await test_client.post('/v1/announcements/', json=payload)
        assert response.status_code == 200

    async def test_02_get_announcements(self, test_client):
        params = {
            'project_code': 'test_01',
            'order': 'asc',
        }
        response = await test_client.get('/v1/announcements/', query_string=params)
        res = response.json()['result'][0]
        assert response.status_code == 200
        assert res['id'] == 1
        assert res['project_code'] == 'test_01'

    async def test_03_post_announcements_message_too_long(self, test_client):
        payload = {
            'project_code': 'test_03',
            'content': (
                'Content for test announcement with a long message. '
                'Rem omnis ea sit. Aliquam omnis tempora est aliquam illo '
                'laborum. Mollitia voluptatem deserunt dolorem sapiente ad '
                'fugit minima tenetur. Atque qui corporis rerum veritatis '
                'aut. Et consectetur aut corporis earum cumque inventore '
                'occaecati rerum.'),
            'publisher': 'erik'
        }
        response = await test_client.post('/v1/announcements/', json=payload)
        assert response.status_code == 400

    async def test_04_get_announcements_no_end_date(self, test_client):
        params = {
            'project_code': 'test_01',
            'start_date': '2022-01-01'
        }
        response = await test_client.get('/v1/announcements/', query_string=params)
        assert response.status_code == 400

    async def test_05_get_announcements_desc(self, test_client):
        params = {
            'project_code': 'test_01',
            'order': 'desc'
        }
        response = await test_client.get('/v1/announcements/', query_string=params)
        res = response.json()['result'][0]
        assert response.status_code == 200
        assert res['id'] == 1
        assert res['project_code'] == 'test_01'

    async def test_06_get_announcements_with_dates(self, test_client):
        params = {
            'project_code': 'test_01',
            'start_date': '2022-01-01 01:01:01',
            'end_date': '2030-12-31 02:02:02'
        }
        response = await test_client.get('/v1/announcements/', query_string=params)
        res = response.json()['result'][0]
        assert response.status_code == 200
        assert res['id'] == 1
        assert res['project_code'] == 'test_01'
