import math

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great-circle distance between two points on the Earth's surface
    using the Haversine formula. Returns distance in kilometers.
    """
    if lat1 is None or lon1 is None or lat2 is None or lon2 is None:
        return 0.0
        
    try:
        lat1, lon1, lat2, lon2 = map(float, [lat1, lon1, lat2, lon2])
        R = 6371.0  # Earth radius in km
        
        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)
        
        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad
        
        a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        return round(R * c, 2)
    except Exception:
        return 0.0

def get_ranked_clinics(clinics_queryset, specialty_id=None, insurance_provider_id=None, city=None, doctor_lat=None, doctor_lng=None):
    """
    Filters and ranks clinics according to:
    Priority 1: Lowest Estimated Wait Time (estimated_wait_days Ascending)
    Priority 2: Nearest Distance (distance Ascending)
    Priority 3: Insurance Compatibility (compatibility Descending)
    """
    # Filter by Specialty
    if specialty_id:
        clinics_queryset = clinics_queryset.filter(specialties__id=specialty_id)
        
    # Filter by Insurance
    if insurance_provider_id:
        clinics_queryset = clinics_queryset.filter(insurance_providers__id=insurance_provider_id)
        
    # Filter by City
    if city:
        clinics_queryset = clinics_queryset.filter(city__icontains=city.strip())
        
    # Remove duplicates from ManyToMany joins
    clinics_queryset = clinics_queryset.distinct()
    
    clinics_list = list(clinics_queryset)
    
    for clinic in clinics_list:
        # Distance calculation
        if doctor_lat is not None and doctor_lng is not None:
            clinic.distance = haversine_distance(doctor_lat, doctor_lng, clinic.latitude, clinic.longitude)
        else:
            clinic.distance = 0.0
            
        # Insurance compatibility calculation
        if insurance_provider_id:
            # If the filter was applied, the clinic is compatible.
            clinic.insurance_compatibility = 1
        else:
            # Otherwise, use count of accepted providers as compatibility strength
            clinic.insurance_compatibility = clinic.insurance_providers.count()
            
    # Multi-level sorting:
    # 1. estimated_wait_days (ascending: lower is better)
    # 2. distance (ascending: closer is better)
    # 3. insurance_compatibility (descending: more compatible is better -> negative for sorting)
    clinics_list.sort(key=lambda c: (
        c.estimated_wait_days, 
        c.distance, 
        -c.insurance_compatibility
    ))
    
    return clinics_list
