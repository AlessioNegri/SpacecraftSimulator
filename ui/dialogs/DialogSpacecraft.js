// ? Saves the parameters of the spacecraft.
function saveParameters()
{
    __Spacecraft.initial_mass                   = _initial_mass_.text
    __Spacecraft.specific_impulse               = _specific_impulse_.text
    __Spacecraft.thrust                         = _thrust_.text
    
    __Spacecraft.lift_coefficient               = _lift_coefficient_.text
    __Spacecraft.drag_coefficient               = _drag_coefficient_.text
    __Spacecraft.reference_surface              = _reference_surface_.text
    __Spacecraft.radiation_pressure_coefficient = _radiation_pressure_coefficient_.text
    __Spacecraft.absorbing_surface              = _absorbing_surface_.text
    
    __Spacecraft.capsule_nose_radius            = _capsule_node_radius_.text
    __Spacecraft.parachute_drag_coefficient     = _parachute_drag_coefficient_.text
    __Spacecraft.parachute_reference_surface    = _parachute_reference_surface_.text
    __Spacecraft.capsule_mass                   = _capsule_mass_.text
    __Spacecraft.capsule_drag_coefficient       = _capsule_drag_coefficient_.text
    __Spacecraft.capsule_lift_coefficient       = _capsule_lift_coefficient_.text
    __Spacecraft.capsule_reference_surface      = _capsule_reference_surface_.text
}

// ? Restores the parameters of the spacecraft.
function restoreParameters()
{
    _initial_mass_.text                     = __Spacecraft.initial_mass
    _specific_impulse_.text                 = __Spacecraft.specific_impulse
    _thrust_.text                           = __Spacecraft.thrust
    
    _lift_coefficient_.text                 = __Spacecraft.lift_coefficient
    _drag_coefficient_.text                 = __Spacecraft.drag_coefficient
    _reference_surface_.text                = __Spacecraft.reference_surface
    _radiation_pressure_coefficient_.text   = __Spacecraft.radiation_pressure_coefficient
    _absorbing_surface_.text                = __Spacecraft.absorbing_surface
    
    _capsule_node_radius_.text              = __Spacecraft.capsule_nose_radius
    _parachute_drag_coefficient_.text       = __Spacecraft.parachute_drag_coefficient
    _parachute_reference_surface_.text      = __Spacecraft.parachute_reference_surface
    _capsule_mass_.text                     = __Spacecraft.capsule_mass
    _capsule_drag_coefficient_.text         = __Spacecraft.capsule_drag_coefficient
    _capsule_lift_coefficient_.text         = __Spacecraft.capsule_lift_coefficient
    _capsule_reference_surface_.text        = __Spacecraft.capsule_reference_surface
}