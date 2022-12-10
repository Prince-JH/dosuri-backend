import coreapi
import coreschema


class ReviewOrderingFilter:
    def get_schema_fields(self, view):
        return [
            coreapi.Field(
                name='page',
                required=False,
                location='query',
                schema=coreschema.Integer(
                    title='Page',
                    description='page'
                )
            )
        ]

    def get_schema_operation_parameters(self, view):
        return [
            {
                'name': 'page',
                'required': False,
                'in': 'query',
                'description': 'page',
                'schema': {
                    'type': 'integer',
                },
            },
        ]
