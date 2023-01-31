class HospitalDistance:
    def get_queryset(self):
        latitude = self.request.GET.get('latitude')
        longitude = self.request.GET.get('longitude')
        if not latitude or not longitude:
            return self.queryset
        return self.queryset.annotate_distance(float(latitude), float(longitude))