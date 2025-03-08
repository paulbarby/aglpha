class CitySerializer:
    """
    Handles serialization and deserialization of City objects.
    """
    @staticmethod
    def serialize_cities(city_manager):
        """Convert all cities to a serializable format"""
        serialized_cities = []
        
        if not city_manager or not hasattr(city_manager, 'cities'):
            return serialized_cities
            
        for city_id, city in city_manager.cities.items():
            serialized_cities.append(CitySerializer.serialize_city(city))
            
        return serialized_cities
    
    @staticmethod
    def serialize_city(city):
        """Convert a single city to a serializable format"""
        return {
            'id': city.id,
            'name': city.name,
            'position': city.position,
            'status': city.status.name if hasattr(city.status, 'name') else str(city.status),
            'population': city.population,
            'resources': city.resources.copy() if hasattr(city, 'resources') else {},
            'buildings': city.buildings.copy() if hasattr(city, 'buildings') else [],
            'production_queue': city.production_queue.copy() if hasattr(city, 'production_queue') else []
            # Add other city attributes as needed
        }
    
    @staticmethod
    def deserialize_cities(city_data, city_manager):
        """Apply serialized city data to a CityManager instance"""
        # This would rebuild all cities from saved data
        # Implementation depends on how cities are constructed
        pass
