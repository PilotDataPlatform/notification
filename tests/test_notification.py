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

from json import loads
import pytest

notificationId = None


class TestNotification():

    @pytest.mark.dependency(name='test_01')
    def test_01_post_notification(self, test_client):
        payload = {
            'type': 'test_01',
            'message': 'Test message from post',
            'detail': {
                'maintenance_date': '2022-01-20T15:20:13.955Z',
                'duration': 1,
                'duration_unit': 'h'},
        }
        response = test_client.post('/v1/notification/', json=payload)
        global notificationId
        notificationId = loads(response.text)['result']['id']
        assert response.status_code == 200

    @pytest.mark.dependency(depends=['test_01'])
    def test_02_get_notification(self, test_client):
        params = {'id': notificationId}
        response = test_client.get('/v1/notification/', params=params)
        assert response.status_code == 200

    @pytest.mark.dependency(depends=['test_01'])
    def test_03_put_notification(self, test_client):
        params = {'id': notificationId}
        payload = {
            'type': 'test_03',
            'message': 'Test message from put',
            'detail': {
                'maintenance_date': '2022-01-20T15:20:13.955Z',
                'duration': 1,
                'duration_unit': 'h'},
        }
        response = test_client.put(
            '/v1/notification/',
            params=params,
            json=payload)
        assert response.status_code == 200

    @pytest.mark.dependency(depends=['test_01'])
    def test_04_get_notifications(self, test_client):
        response = test_client.get('/v1/notifications/')
        assert response.status_code == 200

    @pytest.mark.dependency(depends=['test_01'])
    def test_05_delete_notification(self, test_client):
        params = {'id': notificationId}
        response = test_client.delete('/v1/notification/', params=params)
        assert response.status_code == 200

    @pytest.mark.dependency(name='test_06')
    def test_06_unsubscribe(self, test_client):
        payload = {
            'username': 'erik',
            'notification_id': 1,
        }
        response = test_client.post('/v1/unsubscribe/', json=payload)
        assert response.status_code == 200

    def test_07_get_notification_not_exist(self, test_client):
        params = {'id': '99999'}
        response = test_client.get('/v1/notification/', params=params)
        assert response.status_code == 400

    def test_08_post_notification_message_too_long(self, test_client):
        payload = {
            'type': 'test_08',
            'message': (
                'Test message from post with a long message. '
                'Rem omnis ea sit. Aliquam omnis tempora est aliquam illo '
                'laborum. Mollitia voluptatem deserunt dolorem sapiente ad'
                ' fugit minima tenetur. Atque qui corporis rerum veritatis '
                'aut. Et consectetur aut corporis earum cumque inventore '
                'occaecati rerum.'),
            'detail': {
                'maintenance_date': '2022-01-20T15:20:13.955Z',
                'duration': 1,
                'duration_unit': 'h'},
        }
        response = test_client.post('/v1/notification/', json=payload)
        assert response.status_code == 400

    def test_09_post_notification_duration_not_positive(self, test_client):
        payload = {
            'type': 'test_09',
            'message': 'Test message from post with an invalid duration',
            'detail': {
                'maintenance_date': '2022-01-20T15:20:13.955Z',
                'duration': -1,
                'duration_unit': 'h'},
        }
        response = test_client.post('/v1/notification/', json=payload)
        assert response.status_code == 400

    @pytest.mark.dependency(depends=['test_01'])
    def test_10_put_notification_message_too_long(self, test_client):
        params = {'id': notificationId}
        payload = {
            'type': 'test_10',
            'message': (
                'Test message from put with a long message. Rem omnis ea sit.'
                ' Aliquam omnis tempora est aliquam illo laborum. Mollitia '
                'voluptatem deserunt dolorem sapiente ad fugit minima '
                'tenetur. Atque qui corporis rerum veritatis aut. Et '
                'consectetur aut corporis earum cumque inventore'
                ' occaecati rerum.'),
            'detail': {
                'maintenance_date': '2022-01-20T15:20:13.955Z',
                'duration': 1,
                'duration_unit': 'h'},
        }
        response = test_client.put(
            '/v1/notification/',
            params=params,
            json=payload)
        assert response.status_code == 400

    @pytest.mark.dependency(depends=['test_01'])
    def test_11_put_notification_duration_not_positive(self, test_client):
        params = {'id': notificationId}
        payload = {
            'type': 'test_11',
            'message': 'Test message from put',
            'detail': {
                'maintenance_date': '2022-01-20T15:20:13.955Z',
                'duration': -1,
                'duration_unit': 'h'},
        }
        response = test_client.put(
            '/v1/notification/',
            params=params,
            json=payload)
        assert response.status_code == 400

    def test_12_get_notifications_no_username(self, test_client):
        params = {'all': False}
        response = test_client.get('/v1/notifications/', params=params)
        assert response.status_code == 400

    @pytest.mark.dependency(depends=['test_06'])
    def test_13_get_notifications_with_username(self, test_client):
        params = {
            'all': False,
            'username': 'erik'
        }
        response = test_client.get('/v1/notifications/', params=params)
        assert response.status_code == 200
