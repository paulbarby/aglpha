from src.unit.unit_serializer import UnitSerializer

class UnitManager:
    def __init__(self):
        self.units = {}  # {unit_id: Unit}

    def add_unit(self, unit):
        self.units[unit.id] = unit

    def update_units(self):
        # Update unit behaviors, check movement and combat states, etc.
        for unit in self.units.values():
            # Placeholder: update each unit based on its state
            pass
    
    def serialize(self):
        """Serialize all units using the UnitSerializer"""
        return UnitSerializer.serialize_units(self)
    
    def deserialize(self, unit_data):
        """Deserialize and rebuild units from saved data"""
        return UnitSerializer.deserialize_units(unit_data, self)