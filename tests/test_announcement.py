from fastapi.testclient import TestClient

from app.main import app
from logger import LoggerFactory


class TestAnnouncement:
    log = LoggerFactory(name='test_announcement.log').get_logger()
    app = TestClient(app)

    @classmethod
    def setup_class(cls):
        pass

    @classmethod
    def teardown_class(cls):
        pass

    def test_01_post_announcement(self):
        self.log.info('Test case 1: Post announcement')
        payload = {
            'project_code': 'test_01',
            'content': 'Content for test announcement',
            'publisher': 'erik'
        }
        response = self.app.post('/v1/announcements/', json=payload)
        self.log.info(f'Response payload: {response.text}')
        assert response.status_code == 200
    
    def test_02_get_announcements(self):
        self.log.info(f'Test case 2: Get announcements with projectCode=test_01')
        params = {
            'project_code': 'test_01',
            'order': 'asc',
            'version': '1'
        }
        response = self.app.get('/v1/announcements/', params=params)
        self.log.info(f'Response payload: {response.text}')
        assert response.status_code == 200
    
    def test_03_post_announcements_message_too_long(self):
        self.log.info('Test case 3: Post announcement; message too long')
        payload = {
            'project_code': 'test_03',
            'content': 'Content for test announcement with a long message. Rem omnis ea sit. Aliquam omnis tempora est aliquam illo laborum. Mollitia voluptatem deserunt dolorem sapiente ad fugit minima tenetur. Atque qui corporis rerum veritatis aut. Et consectetur aut corporis earum cumque inventore occaecati rerum.',
            'publisher': 'erik'
        }
        response = self.app.post('/v1/announcements/', json=payload)
        self.log.info(f'Response payload: {response.text}')
        assert response.status_code == 400
    
    def test_04_get_announcements_no_end_date(self):
        self.log.info(f'Test case 4: Get announcements with projectCode=test_01; end date not provided')
        params = {
            'project_code': 'test_01',
            'start_date': '2022-01-01'
        }
        response = self.app.get('/v1/announcements/', params=params)
        self.log.info(f'Response payload: {response.text}')
        assert response.status_code == 400
    
    def test_05_get_announcements_desc(self):
        self.log.info(f'Test case 5: Get announcements with projectCode=test_01; descending order')
        params = {
            'project_code': 'test_01',
            'order': 'desc'
        }
        response = self.app.get('/v1/announcements/', params=params)
        self.log.info(f'Response payload: {response.text}')
        assert response.status_code == 200
    
    def test_06_get_announcements_with_dates(self):
        self.log.info(f'Test case 6: Get announcements with projectCode=test_01; between dates')
        params = {
            'project_code': 'test_01',
            'start_date': '2022-01-01',
            'end_date': '2022-12-31'
        }
        response = self.app.get('/v1/announcements/', params=params)
        self.log.info(f'Response payload: {response.text}')
        assert response.status_code == 200
