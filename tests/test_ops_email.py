import unittest
from unittest.mock import patch
from os import path
import os
from requests import HTTPError
import smtplib
from smtplib import SMTP
from app import create_app


class TestWriteEmails(unittest.TestCase):

    def setUp(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['DEBUG'] = True
        self.app = app.test_client(self)

    def tearDown(self):
        os.system('rm -rf logs')

    def test_post_correct(self):
        payload = {"sender": "notification@vre",
                   "receiver": "jzhang@indocresearch.org",
                   "message": "test email"}
        response = self.app.post("/v1/email", json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertTrue(path.exists('./logs'))

    def test_post_no_sender(self):
        payload = {
            "sender": None,
            "receiver": "jzhang@indocresearch.org",
            "message": "test email"
        }
        response = self.app.post("/v1/email", json=payload)
        self.assertEqual(response.status_code, 400)
        assert b"missing sender or receiver or message" in response.data

    def test_post_no_receiver(self):
        payload = {
            "sender": "notification@vre",
            "receiver": None,
            "message": "test email"
        }
        response = self.app.post("/v1/email", json=payload)
        self.assertEqual(response.status_code, 400)
        assert b"missing sender or receiver or message" in response.data
        import smtplib
        self.assertRaises(smtplib.socket.gaierror)

    def test_post_no_message(self):
        payload = {
            "sender": "notification@vre",
            "receiver": "jzhang@indocresearch.org",
            "message": None
        }
        response = self.app.post("/v1/email", json=payload)
        self.assertEqual(response.status_code, 400)
        assert b"missing sender or receiver or message" in response.data

    def test_html_email(self):
        html_msg = '''<!DOCTYPE html> \
                        <body>\
                        <h4>Dear VRE member,</h4>\
                        </body>\
            </html>'''
        payload = {"sender": "notification@vre",
                   "receiver": "jzhang@indocresearch.org",
                   "message": html_msg,
                   "msg_type": "html"}
        response = self.app.post("/v1/email", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(path.exists('./logs'))

    def test_wrong_message(self):
        payload = {"sender": "notification@vre",
                   "receiver": "jzhang@indocresearch.org",
                   "message": "test message",
                   "msg_type": "csv"}
        response = self.app.post("/v1/email", json=payload)
        self.assertEqual(response.status_code, 400)
        assert b"wrong email type" in response.data

    def test_multiple_receiver_list(self):
        payload = {"sender": "notification@vre",
                   "receiver": ["jzhang@indocresearch.org", "jiayu@indocresearch.org"],
                   "message": "test email"}
        response = self.app.post("/v1/email", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(path.exists('./logs'))

    def test_list_receiver(self):
        payload = {"sender": "notification@vre",
                   "receiver": ["jzhang@indocresearch.org"],
                   "message": "test email"}
        response = self.app.post("/v1/email", json=payload)
        self.assertEqual(response.status_code, 200)

    def test_logs(self):
        self.assertTrue(path.exists('./logs'))

    @patch.object(smtplib, 'SMTP', side_effect=smtplib.socket.gaierror)
    def test_smtp_error(self, mock_smtp_connection_error):
        payload = {"sender": "notification@vre",
                   "receiver": ["jzhang@indocresearch.org"],
                   "message": "test email"}
        response = self.app.post("/v1/email", json=payload)
        self.assertEqual(response.status_code, 500)
        self.assertIsNotNone(response.data)

    @patch.object(SMTP, 'sendmail', side_effect=HTTPError)
    def test_error(self, mock_smtp_send_error):
        payload = {"sender": "notification@vre",
                   "receiver": ["jzhang@indocresearch.org"],
                   "message": "test email"}
        response = self.app.post("/v1/email", json=payload)
        self.assertEqual(response.status_code, 500)
        self.assertIsNotNone(response.data)


if __name__ == "__main__":
    unittest.main()
