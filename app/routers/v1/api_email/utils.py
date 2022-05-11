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
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage

import jinja2
from fastapi.templating import Jinja2Templates

from app.config import ConfigClass
from app.models.base_models import EAPIResponseCode


def allowed_file(filename):
    return '.' in filename and filename.rsplit(
        '.', 1)[1].lower() in ConfigClass.ALLOWED_EXTENSIONS


def is_image(filename):
    return '.' in filename and filename.rsplit(
        '.', 1)[1].lower() in ConfigClass.IMAGE_EXTENSIONS


def validate_email_content(text, template, template_kwargs):
    templates = Jinja2Templates(directory='emails')
    code = EAPIResponseCode.success
    result = ''
    new_text = ''
    if text and template:
        result = 'Please only set text or template, not both'
        code = EAPIResponseCode.bad_request
    if not text and not template:
        result = 'Text or template is required'
        code = EAPIResponseCode.bad_request
    if template:
        try:
            template = templates.get_template(template)
            new_text = template.render(template_kwargs)
        except jinja2.exceptions.TemplateNotFound:
            result = 'Template not found'
            code = EAPIResponseCode.not_found
    return code, result, new_text


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
