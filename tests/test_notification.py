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

    def test_06_unsubscribe(self):
        self.log.info('Test case 6: Unsubscribe from notification with id=1')
        payload = {
            'username': 'erik',
            'notification_id': 1,
        }
        response = self.app.post('/v1/unsubscribe/', json=payload)
        self.log.info(f'Response payload: {response.text}')
        assert response.status_code == 200
