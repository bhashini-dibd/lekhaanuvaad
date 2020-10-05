from flask_restful import fields, marshal_with, reqparse, Resource
from repositories import SentenceRepositories
from models import CustomResponse, Status
import ast

class SentenceGetResource(Resource):
    def get(self, user_id, s_id):
        result  = SentenceRepositories.get_sentence(user_id, s_id)
        if result == False:
            res = CustomResponse(Status.ERR_GLOBAL_MISSING_PARAMETERS.value, None)
            return res.getresjson(), 400

        res = CustomResponse(Status.SUCCESS.value, result)
        return res.getres()

class SentenceBlockGetResource(Resource):
    def get(self, user_id, s_id):
        result  = SentenceRepositories.get_sentence_block(user_id, s_id)
        if result == False:
            res = CustomResponse(Status.ERR_GLOBAL_MISSING_PARAMETERS.value, None)
            return res.getresjson(), 400
        res = CustomResponse(Status.SUCCESS.value, result)
        return result, 200

class SentencePostResource(Resource):
    def post(self, user_id):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('sentences', location='json', type=str, help='sentences cannot be empty', required=True)

        args    = parser.parse_args()
        try:
            sentences = ast.literal_eval(args['sentences'])
        except expression as identifier:
            res = CustomResponse(Status.ERR_GLOBAL_MISSING_PARAMETERS.value,None)
            return res.getresjson(), 400
            
        result = SentenceRepositories.update_sentences(user_id, sentences)
        if result == False:
            res = CustomResponse(Status.ERR_GLOBAL_MISSING_PARAMETERS.value, None)
            return res.getresjson(), 400

        res = CustomResponse(Status.SUCCESS.value, result)
        return res.getres()
