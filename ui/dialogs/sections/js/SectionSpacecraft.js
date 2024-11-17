// >>> Saves the parameters of the dialog.
function saveParameters()
{
    // * Propulsion

    __Spacecraft.initial_mass                   = _initial_mass_.text
    __Spacecraft.specific_impulse               = _specific_impulse_.text
    __Spacecraft.thrust                         = _thrust_.text

    // * Aerodynamics
    
    __Spacecraft.lift_coefficient               = _lift_coefficient_.text
    __Spacecraft.drag_coefficient               = _drag_coefficient_.text
    __Spacecraft.reference_surface              = _reference_surface_.text

    // * Solar Radiation Pressure

    __Spacecraft.radiation_pressure_coefficient = _radiation_pressure_coefficient_.text
    __Spacecraft.absorbing_surface              = _absorbing_surface_.text
}

// >>> Restores the parameters of the dialog.
function restoreParameters()
{
    // * Propulsion

    _initial_mass_.text                     = __Spacecraft.initial_mass
    _specific_impulse_.text                 = __Spacecraft.specific_impulse
    _thrust_.text                           = __Spacecraft.thrust

    // * Aerodynamics
    
    _lift_coefficient_.text                 = __Spacecraft.lift_coefficient
    _drag_coefficient_.text                 = __Spacecraft.drag_coefficient
    _reference_surface_.text                = __Spacecraft.reference_surface

    // * Solar Radiation Pressure

    _radiation_pressure_coefficient_.text   = __Spacecraft.radiation_pressure_coefficient
    _absorbing_surface_.text                = __Spacecraft.absorbing_surface
}