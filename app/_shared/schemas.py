from typing import Any
import bisect

from apiflask import Schema
from apiflask.fields import Integer, String, Nested, Dict, List
from apiflask.validators import Range
from marshmallow.exceptions import ValidationError

from .api_errors import BaseError

ID_FIELD = Integer(allow_none=False, required=True)

class BaseSchema(Schema):
    def handle_error(self, error: ValidationError, data: Any, *, many: bool, **kwargs):
        raise BaseError("Validation Error", error_code=422, payload=error.messages_dict)


def make_response_schema(schema: BaseSchema, is_list=False):
    if is_list:
        class ListResponseSchema(Schema):
            data = List(Nested(schema))
        return ListResponseSchema()
    
    class Response(BaseSchema):
        data = Nested(schema)
    return Response()
    

class PaginationQuery(Schema):
    page = Integer(load_default=1)  # set default page to 1
    per_page = Integer(load_default=20, validate=Range(max=5000))

class SuccessMessage(Schema):
    message = String(default='success')

class GenericSchema(Schema):
    action = String(allow_none=True, required=False)


class Login(BaseSchema):
    email = String(allow_none=False, required=True)
    password = String(allow_none=False, required=True)

class AccessToken(Schema):
    access_token = String()

class ResetPassword(BaseSchema):
    email = String(allow_none=False, required=True)


class ChangePassword(BaseSchema):
    new_password = String(allow_none=False, required=True)
    confirmation_code = String(allow_none=False, required=True)


ResetPasswordSchema = make_response_schema(ResetPassword)
ChangePasswordSchema = make_response_schema(ChangePassword)
LoginSchema = make_response_schema(Login)
AccessTokenSchema  = make_response_schema(AccessToken)


