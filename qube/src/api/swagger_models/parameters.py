from qube.src.api.swagger_models.friday_demo2 \
    import friday_demo2Model, friday_demo2ModelPost

"""
swagger parameters definitions
"""
header_ex = {
    "type": "string",
    "description": "Custom header that is expected as part of the request",
    "name": "Authorization",
    "in": "header",
    "required": False
}

path_ex = {
    "type": "string",
    "description": "This is the part of the URL",
    "name": "entity_id",
    "in": "path",
    "required": True
}

query_ex = {
    "type": "string",
    "description": "Query string appended to the URL",
    "name": "sth",
    "in": "query",
    "required": True
    # "required": False
}

body_ex = {
    'name': 'body',
    'description': 'Request body',
    'in': 'body',
    'schema': friday_demo2Model,
    'required': True,
}

body_post_ex = {
    'name': 'body',
    'description': 'Request body',
    'in': 'body',
    'schema': friday_demo2ModelPost,
    'required': True,
}

body_put_ex = {
    'name': 'body',
    'description': 'Request body',
    'in': 'body',
    'schema': friday_demo2ModelPost,
    'required': True,
}
