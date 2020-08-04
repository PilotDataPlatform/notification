from flask import request, after_this_request
# from flask_restful import Resource
from flask_restx import Api, Resource, fields
import requests
from flask_jwt import jwt_required

from config import ConfigClass
from service_email import api 
import logging
class Ops_email(Resource):
    def __init__(self, **kwargs):
        self.logger = kwargs.get('logger')
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
        try:
            post_data = request.get_json()
            sender = post_data.get('sender', None)
            receiver = post_data.get('receiver', None)
            message = post_data.get('message', None)  
            self.loger.info(f'payload: {post_data}')
            print(receiver);print(message)
            if not sender or not receiver or not message:
                return {'result': 'missing sender or receiver or message'}, 400
            import smtplib
            client = smtplib.SMTP('localhost')
            fromaddr = sender
            toaddrs = receiver
            msg = message
            client.sendmail(fromaddr, [toaddrs], msg)
            client.quit()


        except Exception as e:
            return {'result': str(e)}, 500

        return {'result': "Email sent successfully. "}, 200

