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
import smtplib
from email.header import Header
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from multiprocessing import Process

import jinja2
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi_utils import cbv
from common import LoggerFactory

from app.config import ConfigClass
from app.models.base_models import APIResponse
from app.models.base_models import EAPIResponseCode
from app.models.models_email import POSTEmail
from app.models.models_email import POSTEmailResponse

from .utils import allowed_file
from .utils import is_image

router = APIRouter()
_logger = LoggerFactory('api_emails').get_logger()


def send_emails(
    receivers, sender, subject, text, msg_type, attachments
) -> JSONResponse:
    try:
        client = smtplib.SMTP(
            ConfigClass.POSTFIX_URL,
            ConfigClass.POSTFIX_PORT)
        if ConfigClass.smtp_user and ConfigClass.smtp_pass:
            client.login(ConfigClass.smtp_user, ConfigClass.smtp_pass)
        _logger.info('email server connection established')
    except smtplib.socket.gaierror as e:
        _logger.exception(f'Error connecting with Mail host, {e}')
        api_response = APIResponse()
        api_response.result = str(e)
        api_response.code = EAPIResponseCode.internal_error
        return api_response.json_response()

    for to in receivers:
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = to
        msg['Subject'] = Header(subject, 'utf-8')
        for attachment in attachments:
            msg.attach(attachment)

        if msg_type == 'plain':
            msg.attach(MIMEText(text, 'plain', 'utf-8'))
        else:
            msg.attach(MIMEText(text, 'html', 'utf-8'))

        try:
            _logger.info(
                f"\nto: {to}\nfrom: {sender}\nsubject: {msg['Subject']}")
            client.sendmail(sender, to, msg.as_string())
        except Exception as e:
            _logger.exception(f'Error when sending email to {to}, {e}')
            api_response = APIResponse()
            api_response.result = str(e)
            api_response.code = EAPIResponseCode.internal_error
            return api_response.json_response()
    client.quit()


@cbv.cbv(router)
class WriteEmails:
    @router.post('/', response_model=POSTEmailResponse, summary='Send emails')
    async def post(self, data: POSTEmail):
        api_response = POSTEmailResponse()
        text = data.message
        template = data.template
        code, result = validate_email_content(
            text,
            template,
            data.template_kwargs)
        if result:
            api_response.result = result
            api_response.code = code
            return api_response.json_response()
        attachments = []
        for file in data.attachments:
            code, attach, attach = attach_data(file)
            if code != EAPIResponseCode.success:
                api_response.result = result
                api_response.code = code
                return api_response.json_response()
            else:
                attachments.append(attach)
        if data.msg_type not in ['html', 'plain']:
            api_response.result = 'wrong email type'
            api_response.code = EAPIResponseCode.bad_request
            return api_response.json_response()

        log_data = data.__dict__.copy()
        if log_data.get('attachments'):
            del log_data['attachments']
        _logger.info(f'payload: {log_data}')
        _logger.info(f'receiver: {data.receiver}')
        # Open the SMTP connection just to test that
        # it's working before doing the real sending in the background
        try:
            client = smtplib.SMTP(
                ConfigClass.POSTFIX_URL,
                ConfigClass.POSTFIX_PORT)
            if ConfigClass.smtp_user and ConfigClass.smtp_pass:
                client.login(ConfigClass.smtp_user, ConfigClass.smtp_pass)
            _logger.info('email server connection established')
        except smtplib.socket.gaierror as e:
            api_response.result = str(e)
            api_response.code = EAPIResponseCode.internal_error
            return api_response.json_response()
        client.quit()

        p = Process(
            target=send_emails,
            args=(
                data.receiver,
                data.sender,
                data.subject,
                text,
                data.msg_type,
                attachments),
        )
        p.daemon = True
        p.start()
        _logger.info(f'Email sent successfully to {data.receiver}')
        api_response.result = 'Email sent successfully. '
        return api_response.json_response()


def validate_email_content(text, template, template_kwargs):
    templates = Jinja2Templates(directory='emails')
    code = EAPIResponseCode.success
    result = ''
    if text and template:
        result = 'Please only set text or template, not both'
        code = EAPIResponseCode.bad_request
    if not text and not template:
        _logger.exception('Text or template is required')
        result = 'Text or template is required'
        code = EAPIResponseCode.bad_request
    if template:
        try:
            template = templates.get_template(template)
            text = template.render(template_kwargs)
        except jinja2.exceptions.TemplateNotFound:
            result = 'Template not found'
            code = EAPIResponseCode.not_found
    return code, result


def attach_data(file):
    code = EAPIResponseCode.success
    result = ''
    if ',' in file.get('data'):
        attach_data = base64.b64decode(file.get('data').split(',')[1])
    else:
        attach_data = base64.b64decode(file.get('data'))

    # check if bigger to 2mb
    if len(attach_data) > 2000000:
        result = 'attachement to large'
        code = EAPIResponseCode.to_large
        attach = None
        return code, result, attach

    filename = file.get('name')
    if not allowed_file(filename):
        result = 'File type not allowed'
        code = EAPIResponseCode.bad_request
        attach = None
        return code, result, attach

    if attach_data and allowed_file(filename):
        if is_image(filename):
            attach = MIMEImage(attach_data)
            attach.add_header(
                'Content-Disposition',
                'attachment',
                filename=filename)
        else:
            attach = MIMEApplication(
                attach_data,
                _subtype='pdf',
                filename=filename)
            attach.add_header(
                'Content-Disposition',
                'attachment',
                filename=filename)
        return code, result, attach
