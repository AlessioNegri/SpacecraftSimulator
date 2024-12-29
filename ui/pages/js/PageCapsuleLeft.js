// ? Saves the parameters of the dialog.
function saveParameters()
{   
    // * Structure

    __Capsule.capsule_mass                  = _capsule_mass_.text 
    __Capsule.capsule_nose_radius           = _capsule_node_radius_.text

    // * Aerodynamics

    __Capsule.capsule_lift_coefficient      = _capsule_lift_coefficient_.text
    __Capsule.capsule_drag_coefficient      = _capsule_drag_coefficient_.text
    __Capsule.capsule_reference_surface     = _capsule_reference_surface_.text

    // * Parachute

    __Capsule.parachute_drag_coefficient    = _parachute_drag_coefficient_.text
    __Capsule.parachute_reference_surface   = _parachute_reference_surface_.text
}

// ? Restores the parameters of the dialog.
function restoreParameters()
{   
    // * Structure

    _capsule_mass_.text                 = __Capsule.capsule_mass 
    _capsule_node_radius_.text          = __Capsule.capsule_nose_radius

    // * Aerodynamics

    _capsule_lift_coefficient_.text     = __Capsule.capsule_lift_coefficient
    _capsule_drag_coefficient_.text     = __Capsule.capsule_drag_coefficient
    _capsule_reference_surface_.text    = __Capsule.capsule_reference_surface

    // * Parachute

    _parachute_drag_coefficient_.text   = __Capsule.parachute_drag_coefficient
    _parachute_reference_surface_.text  = __Capsule.parachute_reference_surface
}