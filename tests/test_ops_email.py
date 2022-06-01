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

import base64
import os
import platform
from os import path
from unittest.mock import MagicMock


class TestWriteEmails:
    post_api = '/v1/email/'
    TEST_EMAIL_SENDER = 'sender@test.com'
    TEST_EMAIL_RECEIVER = 'receiver@test.com'
    TEST_EMAIL_RECEIVER_2 = 'receiver2@test.com'

    def test_post_correct(self, test_client_email, smtp_mocker: MagicMock, mock_multiprocessing_process):
        payload = {
            'sender': self.TEST_EMAIL_SENDER,
            'receiver': [self.TEST_EMAIL_RECEIVER],
            'message': 'Test email contents',
        }
        response = test_client_email.post(self.post_api, json=payload)
        assert response.status_code == 200
        assert smtp_mocker.call_count == 2
        assert smtp_mocker.return_value.login.call_count == 2
        assert smtp_mocker.return_value.sendmail.call_count == 1

    def test_post_no_sender(self, test_client_email):
        payload = {
            'sender': None,
            'receiver': self.TEST_EMAIL_RECEIVER,
            'message': 'test email'}
        response = test_client_email.post(self.post_api, json=payload)
        assert response.status_code == 422
        assert b'none is not an allowed value' in response.content

    def test_post_no_receiver(self, test_client_email):
        payload = {
            'sender': self.TEST_EMAIL_SENDER,
            'receiver': None,
            'message': 'test email'}
        response = test_client_email.post(self.post_api, json=payload)
        assert response.status_code == 422
        assert b'none is not an allowed value' in response.content

    def test_post_no_message(self, test_client_email):
        payload = {
            'sender': self.TEST_EMAIL_SENDER,
            'receiver': [self.TEST_EMAIL_RECEIVER],
        }
        response = test_client_email.post(self.post_api, json=payload)
        assert response.status_code == 400
        assert b'Text or template is required' in response.content

    def test_html_email(self, test_client_email, smtp_mocker: MagicMock, mock_multiprocessing_process):
        html_msg = '''<!DOCTYPE html> \
                        <body>\
                        <h4>Dear member,</h4>\
                        </body>\
            </html>'''
        payload = {
            'sender': self.TEST_EMAIL_SENDER,
            'receiver': [self.TEST_EMAIL_RECEIVER],
            'message': html_msg,
            'msg_type': 'html',
        }
        response = test_client_email.post(self.post_api, json=payload)
        assert response.status_code == 200
        assert smtp_mocker.call_count == 2
        assert smtp_mocker.return_value.login.call_count == 2
        assert smtp_mocker.return_value.sendmail.call_count == 1

    def test_wrong_message(self, test_client_email):
        payload = {
            'sender': self.TEST_EMAIL_SENDER,
            'receiver': [self.TEST_EMAIL_RECEIVER],
            'message': 'test message',
            'msg_type': 'csv',
        }
        response = test_client_email.post(self.post_api, json=payload)
        assert response.status_code == 400
        assert b'wrong email type' in response.content

    def test_multiple_receiver_list(self, test_client_email, smtp_mocker: MagicMock, mock_multiprocessing_process):
        payload = {
            'sender': self.TEST_EMAIL_SENDER,
            'receiver': [self.TEST_EMAIL_RECEIVER, self.TEST_EMAIL_RECEIVER_2],
            'message': 'test email',
        }
        response = test_client_email.post(self.post_api, json=payload)
        assert response.status_code == 200
        assert smtp_mocker.call_count == 2
        assert smtp_mocker.return_value.login.call_count == 2
        assert smtp_mocker.return_value.sendmail.call_count == 2

    def test_list_receiver(self, test_client_email, smtp_mocker: MagicMock, mock_multiprocessing_process):
        payload = {
            'sender': self.TEST_EMAIL_SENDER,
            'receiver': [self.TEST_EMAIL_RECEIVER],
            'message': 'test email',
        }
        response = test_client_email.post(self.post_api, json=payload)
        assert response.status_code == 200
        assert smtp_mocker.call_count == 2
        assert smtp_mocker.return_value.login.call_count == 2
        assert smtp_mocker.return_value.sendmail.call_count == 1

    def test_logs(self):
        assert os.path.exists('./logs') is True

    def test_smtp_error(self, test_client_email, mock_multiprocessing_process, smtp_mocker_connection_error: MagicMock):
        payload = {
            'sender': self.TEST_EMAIL_SENDER,
            'receiver': [self.TEST_EMAIL_RECEIVER],
            'message': 'test email',
        }
        response = test_client_email.post(self.post_api, json=payload)
        assert response.status_code == 500
        assert response.content is not None

    def test_send_email_with_png_attachment(self, test_client_email, mock_multiprocessing_process,
                                            smtp_mocker: MagicMock):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        png_path = dir_path + '/test1.png'
        if not path.isfile(png_path):
            os.system('touch ' + png_path)

        with open(png_path, 'rb') as img:
            payload = {
                'sender': self.TEST_EMAIL_SENDER,
                'receiver': [self.TEST_EMAIL_RECEIVER],
                'message': 'test email',
                'subject': 'test email',
                'msg_type': 'plain',
                'attachments': [
                    {

                        'name': png_path,
                        'data': base64.b64encode(
                            img.read() + b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00IEND\xaeB`\x82').decode(
                            'utf-8')}],
            }
            response = test_client_email.post(self.post_api, json=payload)
            assert response.status_code == 200
            assert smtp_mocker.call_count == 2
            assert smtp_mocker.return_value.login.call_count == 2
            assert smtp_mocker.return_value.sendmail.call_count == 1
            os.system('rm ' + png_path)

    def test_send_email_with_multiple_attachments(self, test_client_email, mock_multiprocessing_process,
                                                  smtp_mocker: MagicMock):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        pdf_path = dir_path + '/test2.pdf'
        jpg_path = dir_path + '/test3.jpg'
        jpeg_path = dir_path + '/test4.jpeg'
        gif_path = dir_path + '/test5.gif'
        if (
                not path.isfile(pdf_path)
                or not path.isfile(jpg_path)
                or not path.isfile(jpeg_path)
                or not path.isfile(gif_path)
        ):
            os.system('touch ' + pdf_path)
            os.system('touch ' + jpg_path)
            os.system('touch ' + jpeg_path)
            os.system('touch ' + gif_path)

        with open(pdf_path, 'rb') as img1:
            with open(jpg_path, 'rb') as img2:
                with open(jpeg_path, 'rb') as img3:
                    with open(gif_path, 'rb') as img4:
                        payload = {
                            'sender': self.TEST_EMAIL_SENDER,
                            'receiver': [self.TEST_EMAIL_RECEIVER],
                            'message': 'test email',
                            'subject': 'test email',
                            'msg_type': 'plain',
                            'attachments': [
                                {
                                    'name': pdf_path,
                                    'data': base64.b64encode(
                                        img1.read() + b'\x89PDF\r\n\x1a\n\x00\rIHDR\x00\x00IEND\xaeB`\x82').decode(
                                        'utf-8')},
                                {
                                    'name': jpg_path,
                                    'data': base64.b64encode(
                                        img2.read() + b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x00\x00?\xff\xd9').decode(
                                        'utf-8')},
                                {
                                    'name': jpeg_path,
                                    'data': base64.b64encode(
                                        img3.read() + b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x00\x00?\xff\xd9').decode(
                                        'utf-8')},
                                {
                                    'name': gif_path,
                                    'data': base64.b64encode(
                                        img4.read() + b'GIF89a,\x01,\x01\xf7\x13\x00\xff\x95\x99]f\x85d\x00;').decode(
                                        'utf-8')},
                            ],
                        }
                        response = test_client_email.post(
                            self.post_api,
                            json=payload)
                        assert response.status_code == 200
                        assert smtp_mocker.call_count == 2
                        assert smtp_mocker.return_value.login.call_count == 2
                        assert smtp_mocker.return_value.sendmail.call_count == 1
                        os.system('rm ' + pdf_path)
                        os.system('rm ' + jpg_path)
                        os.system('rm ' + jpeg_path)
                        os.system('rm ' + gif_path)

    def test_send_email_with_unsupport_attachment(self, test_client_email, mock_multiprocessing_process,
                                                  smtp_mocker: MagicMock):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        xml_path = dir_path + '/invalid.xml'

        if not path.isfile(xml_path):
            os.system('touch ' + xml_path)

        with open(xml_path, 'rb') as img:
            payload = {
                'sender': self.TEST_EMAIL_SENDER,
                'receiver': [self.TEST_EMAIL_RECEIVER],
                'message': 'test email',
                'subject': 'test email',
                'msg_type': 'plain',
                'attachments': [
                    {
                        'name': 'invalid.xml',
                        'data': base64.b64encode(img.read()).decode('utf-8')}],
            }
            response = test_client_email.post(self.post_api, json=payload)
            assert smtp_mocker.call_count == 0
            assert smtp_mocker.return_value.login.call_count == 0
            assert response.status_code == 400
            os.system('rm ' + xml_path)

    def test_send_email_with_large_attachment(self, test_client_email, mock_multiprocessing_process,
                                              smtp_mocker: MagicMock):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        large_file_path = dir_path + '/invalid_large.pdf'

        if not path.isfile(large_file_path):
            if platform.system() == 'Darwin':
                os.system('mkfile -n 2.5M ' + large_file_path)
            else:
                os.system('fallocate -l 2.5M ' + large_file_path)

        with open(large_file_path, 'rb') as img:
            payload = {
                'sender': self.TEST_EMAIL_SENDER,
                'receiver': [self.TEST_EMAIL_RECEIVER],
                'message': 'test email',
                'subject': 'test email',
                'msg_type': 'plain',
                'attachments': [
                    {
                        'name': 'invalid_large.pdf',
                        'data': base64.b64encode(img.read()).decode('utf-8')
                    }
                ],
            }
            response = test_client_email.post(self.post_api, json=payload)
            assert smtp_mocker.call_count == 0
            assert smtp_mocker.return_value.login.call_count == 0
            assert response.status_code == 413
            os.system('rm ' + large_file_path)
