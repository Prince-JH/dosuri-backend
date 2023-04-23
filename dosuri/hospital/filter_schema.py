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
                    'type': 'string',
                },
            },
        ]


class HospitalDistanceFilterSchema:
    def get_schema_fields(self, view):
        return [
            coreapi.Field(
                name=param, location='query', required=False,
                schema=coreschema.String(title=f'{param} of user',
                                         description=f'{param} of user')
            )
            for param
            in view.hospital_distance_filter_params if param != 'distance'
        ]

    def get_schema_operation_parameters(self, view):
        return [
            {
                'name': param,
                'in': 'query',
                'required': False,
                'description': f'{param} of user',
                'schema': {'type': 'float'}
            }
            for param
            in view.hospital_distance_filter_params if param != 'distance'
        ]


class AvgPricePerHourFilterSchema:
    def get_schema_fields(self, view):
        return [
            coreapi.Field(
                name='price_range_from', location='query', required=False,
                schema=coreschema.String(title=f'lower limit of average price per hour',
                                         description=f'lower limit of average price per hour')
            ),
            coreapi.Field(
                name='price_range_to', location='query', required=False,
                schema=coreschema.String(title=f'upper limit of average price per hour',
                                         description=f'upper limit of average price per hour')
            )
        ]

    def get_schema_operation_parameters(self, view):
        return [
            {
                'name': 'price_range_from',
                'required': False,
                'in': 'query',
                'description': 'lower limit of average price per hour',
                'schema': {
                    'type': 'integer',
                },
            },
            {
                'name': 'price_range_to',
                'required': False,
                'in': 'query',
                'description': 'upper limit of average price per hour',
                'schema': {
                    'type': 'integer',
                },
            },
        ]
