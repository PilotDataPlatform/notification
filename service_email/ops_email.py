from flask import request, after_this_request, current_app
# from flask_restful import Resource
from flask_restx import Api, Resource, fields
import requests
from flask_jwt import jwt_required
import smtplib
from config import ConfigClass
from service_email import api 
import logging

class Ops_email(Resource):
    # user login 
    ################################################################# Swagger
    query_payload = api.model(
        "query_payload_basic", {
            "sender": fields.String(readOnly=True, description='sender'),
            "receiver": fields.String(readOnly=True, description='receiver'),
            "message": fields.String(readOnly=True, description='message'),
        }
    )
    query_sample_return = '''
    # Below are the sample return
    {
        "result": {"Email sent successfully"}
    }
    '''
    #################################################################
    @api.expect(query_payload)
    @api.response(200, query_sample_return)
    def post(self):
        current_app.logger.info('received request')
        post_data = request.get_json()
        sender = post_data.get('sender', None)
        receiver = post_data.get('receiver', None)
        message = post_data.get('message', None)  
        current_app.logger.info(f'payload: {post_data}')
        current_app.logger.info(f'receiver: {receiver}')
        current_app.logger.info(f'message: {message}')
        if not sender or not receiver or not message:
            current_app.logger.exception('missing sender or receiver or message')
            return {'result': 'missing sender or receiver or message'}, 400
        try:
            client = smtplib.SMTP_SSL(ConfigClass.postfix,25)
            # client.ehlo()
            # client.starttls()
            # # client.connect()
            client.login(ConfigClass.smtp_user, ConfigClass.smtp_pass)
            current_app.logger.info('email server connection established')
        except smtplib.socket.gaierror as e:
            current_app.logger.exception(f'Error connecting with Mail host, {e}')
            return {'result': str(e)}, 500
        fromaddr = sender
        toaddrs = receiver
        msg = message
        try:    
            client.sendmail(fromaddr, [toaddrs], msg)
        except Exception as e:
            current_app.logger.exception(f'Error when sending email to {receiver}, {e}')
            return {'result': str(e)}, 500
        client.quit()
        current_app.logger.info(f'Email sent successfully to {receiver}')
        return {'result': "Email sent successfully. "}, 200

