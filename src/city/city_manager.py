from src.city.city_serializer import CitySerializer

class CityManager:
    def __init__(self):
        self.cities = {}  # {city_id: City}

    def add_city(self, city):
        self.cities[city.id] = city

    def update_cities(self):
        # Update resource collection, growth, and production in each city
        for city in self.cities.values():
            # Placeholder: update city status and resources
            pass
    
    def serialize(self):
        """Serialize all cities using the CitySerializer"""
        return CitySerializer.serialize_cities(self)
    
    def deserialize(self, city_data):
        """Deserialize and rebuild cities from saved data"""
        return CitySerializer.deserialize_cities(city_data, self)