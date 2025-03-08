class UnitSerializer:
    """
    Handles serialization and deserialization of Unit objects.
    """
    @staticmethod
    def serialize_units(unit_manager):
        """Convert all units to a serializable format"""
        serialized_units = []
        
        if not unit_manager or not hasattr(unit_manager, 'units'):
            return serialized_units
            
        for unit_id, unit in unit_manager.units.items():
            serialized_units.append(UnitSerializer.serialize_unit(unit))
            
        return serialized_units
    
    @staticmethod
    def serialize_unit(unit):
        """Convert a single unit to a serializable format"""
        return {
            'id': unit.id,
            'unit_type': unit.unit_type,
            'position': unit.position,
            'state': unit.state.name if hasattr(unit.state, 'name') else str(unit.state),
            'health': unit.health,
            'attack_power': unit.attack_power,
            'defense': unit.defense,
            'move_range': unit.move_range
            # Add other unit attributes as needed
        }
    
    @staticmethod
    def deserialize_units(unit_data, unit_manager):
        """Apply serialized unit data to a UnitManager instance"""
        # This would rebuild all units from saved data
        # Implementation depends on how units are constructed
        pass
