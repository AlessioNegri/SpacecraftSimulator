// ? Saves the parameters of the dialog.
function saveParameters()
{   
    // * Structure

    __Capsule.capsule_mass                          = _capsule_mass_.text 
    __Capsule.capsule_nose_radius                   = _capsule_nose_radius_.text
    __Capsule.capsule_body_radius                   = _capsule_body_radius_.text
    __Capsule.capsule_shield_angle                  = _capsule_shield_angle_.text
    __Capsule.capsule_afterbody_angle               = _capsule_afterbody_angle_.text

    // * Aerodynamics

    __Capsule.specific_heat_ratio                   = _specific_heat_ratio_.text
    __Capsule.capsule_zero_lift_drag_coefficient    = _capsule_zero_lift_drag_coefficient_.text
    __Capsule.capsule_lift_coefficient              = _capsule_lift_coefficient_.text
    __Capsule.capsule_drag_coefficient              = _capsule_drag_coefficient_.text
    __Capsule.capsule_reference_surface             = _capsule_reference_surface_.text
    __Capsule.capsule_angle_of_attack               = _capsule_angle_of_attack_.text

    // * Parachute

    __Capsule.parachute_drag_coefficient            = _parachute_drag_coefficient_.text
    __Capsule.parachute_reference_surface           = _parachute_reference_surface_.text
}

// ? Restores the parameters of the dialog.
function restoreParameters()
{   
    // * Structure

    _capsule_mass_.text                         = __Capsule.capsule_mass 
    _capsule_nose_radius_.text                  = __Capsule.capsule_nose_radius
    _capsule_body_radius_.text                  = __Capsule.capsule_body_radius
    _capsule_shield_angle_.text                 = __Capsule.capsule_shield_angle
    _capsule_afterbody_angle_.text              = __Capsule.capsule_afterbody_angle

    // * Aerodynamics

    _specific_heat_ratio_.text                  = __Capsule.specific_heat_ratio
    _capsule_zero_lift_drag_coefficient_.text   = __Capsule.capsule_zero_lift_drag_coefficient
    _capsule_lift_coefficient_.text             = __Capsule.capsule_lift_coefficient
    _capsule_drag_coefficient_.text             = __Capsule.capsule_drag_coefficient
    _capsule_reference_surface_.text            = __Capsule.capsule_reference_surface
    _capsule_angle_of_attack_.text              = __Capsule.capsule_angle_of_attack

    // * Parachute

    _parachute_drag_coefficient_.text           = __Capsule.parachute_drag_coefficient
    _parachute_reference_surface_.text          = __Capsule.parachute_reference_surface
}

// ? Reloads the Aerodynamic Coefficients C_L and C_D
function reloadAerodynamicCoefficients()
{
    _capsule_lift_coefficient_.text             = __Capsule.capsule_lift_coefficient
    _capsule_drag_coefficient_.text             = __Capsule.capsule_drag_coefficient
}