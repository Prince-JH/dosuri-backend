import coreapi
import coreschema


# class AddressFilter:
#     def get_schema_fields(self, view):
#         return [
#             coreapi.Field(
#                 name=f'address',
#                 location='query', required=False,
#                 schema=coreschema.String(title='address that you are trying to query',
#                                          description='Query in Korean without unit ex) 서울시 x 서울 o'),
#             )
#         ]
#
#     def get_schema_operation_parameters(self, view):
#         return [
#             {
#                 'name': f'address',
#                 'in': 'query',
#                 'required': False,
#                 'description': 'Query in Korean without unit ex) 서울시 x 서울 o',
#                 'schema': {'type': 'string'},
#             },
#         ]

class ForeignUuidFilter:
    def get_schema_fields(self, view):
        return [
            coreapi.Field(
                name=param, location='query', required=False,
                schema=coreschema.String(title=f'uuid of {param}',
                                         description=f'uuid of {param}')
            )
            for param
            in view.uuid_filter_params
        ]

    def get_schema_operation_parameters(self, view):
        return [
            {
                'name': param,
                'in': 'query',
                'required': False,
                'description': f'uuid of {param}',
                'schema': {'type': 'string'}
            }
            for param
            in view.uuid_filter_params
        ]


class UuidSetFilter:
    def get_schema_fields(self, view):
        return [
            coreapi.Field(
                name='uuid_set', location='query', required=False,
                schema=coreschema.String(title=f'uuid set',
                                         description='uuid set to query at once.<br>' \
                                                     '<code>/?uuid_set=<uuid_1>&uuid_set=<uuid_2>&uuid_set=<uuid_3></code> would return resource 1,2,3 altogether.')
            )
        ]

    def get_schema_operation_parameters(self, view):
        return [
            {
                'name': 'uuid_set',
                'in': 'query',
                'required': False,
                'description': 'uuid set to query at once.<br>' \
                               '<code>/?uuid_set=<uuid_1>&uuid_set=<uuid_2>&uuid_set=<uuid_3></code> would return resource 1,2,3 altogether.',
                'schema': {
                    'type': 'string',
                }
            }
        ]
