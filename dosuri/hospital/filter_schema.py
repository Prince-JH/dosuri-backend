import coreapi
import coreschema


class PageQueryParamFilterSchema:
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


class DoctorPositionFilterSchema:
    def get_schema_fields(self, view):
        return [
            coreapi.Field(
                name='position',
                required=False,
                location='query',
                schema=coreschema.String(
                    title='Position',
                    description='position'
                )
            )
        ]

    def get_schema_operation_parameters(self, view):
        return [
            {
                'name': 'position',
                'required': False,
                'in': 'query',
                'description': 'position',
                'schema': {
                    'type': 'position',
                },
            },
        ]
