from json import loads

import pytest
from fastapi.testclient import TestClient

from app.main import app
from tests.logger import Logger

notificationId = None


class TestNotification:
    log = Logger(name='test_notification.log')
    app = TestClient(app)

    @classmethod
    def setup_class(cls):
        pass

    @classmethod
    def teardown_class(cls):
        pass

    @pytest.mark.dependency(name='test_01')
    def test_01_post_notification(self):
        self.log.info('Test case 1: Post notification')
        payload = {
            'type': 'test_01',
            'message': 'Test message from post',
            'detail': {'maintenance_date': '2022-01-20T15:20:13.955Z', 'duration': 1, 'duration_unit': 'h'},
        }
        response = self.app.post('/v1/notification/', json=payload)
        self.log.info(f'Response payload: {response.text}')
        global notificationId
        notificationId = loads(response.text)['result']['id']
        assert response.status_code == 200
    
    @pytest.mark.dependency(depends=['test_01'])
    def test_02_get_notification(self):
        self.log.info(f'Test case 2: Get notification with id={notificationId}')
        params = {'id': notificationId}
        response = self.app.get('/v1/notification/', params=params)
        self.log.info(f'Response payload: {response.text}')
        assert response.status_code == 200

    @pytest.mark.dependency(depends=['test_01'])
    def test_03_put_notification(self):
        self.log.info(f'Test case 3: Put notification with id={notificationId}')
        params = {'id': notificationId}
        payload = {
            'type': 'test_03',
            'message': 'Test message from put',
            'detail': {'maintenance_date': '2022-01-20T15:20:13.955Z', 'duration': 1, 'duration_unit': 'h'},
        }
        response = self.app.put('/v1/notification/', params=params, json=payload)
        self.log.info(f'Response payload: {response.text}')
        assert response.status_code == 200

    @pytest.mark.dependency(depends=['test_01'])
    def test_04_get_notifications(self):
        self.log.info('Test case 4: Get many notifications')
        response = self.app.get('/v1/notifications/')
        self.log.info(f'Response payload: {response.text}')
        assert response.status_code == 200

    @pytest.mark.dependency(depends=['test_01'])
    def test_05_delete_notification(self):
        self.log.info(f'Test case 5: Delete notification with id={notificationId}')
        params = {'id': notificationId}
        response = self.app.delete('/v1/notification/', params=params)
        self.log.info(f'Response payload: {response.text}')
        assert response.status_code == 200

    @pytest.mark.dependency(name='test_06')
    def test_06_unsubscribe(self):
        self.log.info('Test case 6: Unsubscribe from notification with id=1')
        payload = {
            'username': 'erik',
            'notification_id': 1,
        }
        response = self.app.post('/v1/unsubscribe/', json=payload)
        self.log.info(f'Response payload: {response.text}')
        assert response.status_code == 200

    def test_07_get_notification_not_exist(self):
        self.log.info(f'Test case 7: Get notification with id=99999')
        params = {'id': '99999'}
        response = self.app.get('/v1/notification/', params=params)
        self.log.info(f'Response payload: {response.text}')
        assert response.status_code == 400
    
    def test_08_post_notification_message_too_long(self):
        self.log.info('Test case 8: Post notification; message too long')
        payload = {
            'type': 'test_08',
            'message': 'Test message from post with a long message. Rem omnis ea sit. Aliquam omnis tempora est aliquam illo laborum. Mollitia voluptatem deserunt dolorem sapiente ad fugit minima tenetur. Atque qui corporis rerum veritatis aut. Et consectetur aut corporis earum cumque inventore occaecati rerum.',
            'detail': {'maintenance_date': '2022-01-20T15:20:13.955Z', 'duration': 1, 'duration_unit': 'h'},
        }
        response = self.app.post('/v1/notification/', json=payload)
        self.log.info(f'Response payload: {response.text}')
        assert response.status_code == 400

    def test_09_post_notification_duration_not_positive(self):
        self.log.info('Test case 9: Post notification; duration not positive')
        payload = {
            'type': 'test_09',
            'message': 'Test message from post with an invalid duration',
            'detail': {'maintenance_date': '2022-01-20T15:20:13.955Z', 'duration': -1, 'duration_unit': 'h'},
        }
        response = self.app.post('/v1/notification/', json=payload)
        self.log.info(f'Response payload: {response.text}')
        assert response.status_code == 400

    @pytest.mark.dependency(depends=['test_01'])
    def test_10_put_notification_message_too_long(self):
        self.log.info(f'Test case 10: Put notification with id={notificationId}; message too long')
        params = {'id': notificationId}
        payload = {
            'type': 'test_10',
            'message': 'Test message from put with a long message. Rem omnis ea sit. Aliquam omnis tempora est aliquam illo laborum. Mollitia voluptatem deserunt dolorem sapiente ad fugit minima tenetur. Atque qui corporis rerum veritatis aut. Et consectetur aut corporis earum cumque inventore occaecati rerum.',
            'detail': {'maintenance_date': '2022-01-20T15:20:13.955Z', 'duration': 1, 'duration_unit': 'h'},
        }
        response = self.app.put('/v1/notification/', params=params, json=payload)
        self.log.info(f'Response payload: {response.text}')
        assert response.status_code == 400

    @pytest.mark.dependency(depends=['test_01'])
    def test_11_put_notification_duration_not_positive(self):
        self.log.info(f'Test case 10: Put notification with id={notificationId}; duration not positive')
        params = {'id': notificationId}
        payload = {
            'type': 'test_11',
            'message': 'Test message from put',
            'detail': {'maintenance_date': '2022-01-20T15:20:13.955Z', 'duration': -1, 'duration_unit': 'h'},
        }
        response = self.app.put('/v1/notification/', params=params, json=payload)
        self.log.info(f'Response payload: {response.text}')
        assert response.status_code == 400

    def test_12_get_notifications_no_username(self):
        self.log.info('Test case 12: Get many notifications; username not provided')
        params = {'all': False}
        response = self.app.get('/v1/notifications/', params=params)
        self.log.info(f'Response payload: {response.text}')
        assert response.status_code == 400

    @pytest.mark.dependency(depends=['test_06'])
    def test_13_get_notifications_with_username(self):
        self.log.info('Test case 13: Get many notifications; with username')
        params = {
            'all': False,
            'username': 'erik'
        }
        response = self.app.get('/v1/notifications/', params=params)
        self.log.info(f'Response payload: {response.text}')
        assert response.status_code == 200
