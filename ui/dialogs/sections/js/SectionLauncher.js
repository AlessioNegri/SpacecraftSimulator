// >>> Saves the parameters of the dialog.
function saveParameters()
{   
    // * Structure

    __MissionOrbitInsertion.stage_1.structural_mass             = _structural_mass_1_.text 
    __MissionOrbitInsertion.stage_1.propellant_mass             = _propellant_mass_1_.text
    __MissionOrbitInsertion.stage_1.diameter                    = _diameter_1_.text
    __MissionOrbitInsertion.stage_1.gross_mass                  = _gross_mass_1_.text
    __MissionOrbitInsertion.stage_1.payload_mass                = _payload_mass_1_.text
    __MissionOrbitInsertion.stage_1.total_mass                  = _total_mass_1_.text

    __MissionOrbitInsertion.stage_2.structural_mass             = _structural_mass_2_.text 
    __MissionOrbitInsertion.stage_2.propellant_mass             = _propellant_mass_2_.text
    __MissionOrbitInsertion.stage_2.diameter                    = _diameter_2_.text
    __MissionOrbitInsertion.stage_2.gross_mass                  = _gross_mass_2_.text
    __MissionOrbitInsertion.stage_2.payload_mass                = _payload_mass_2_.text
    __MissionOrbitInsertion.stage_2.total_mass                  = _total_mass_2_.text

    __MissionOrbitInsertion.stage_3.structural_mass             = _structural_mass_3_.text 
    __MissionOrbitInsertion.stage_3.propellant_mass             = _propellant_mass_3_.text
    __MissionOrbitInsertion.stage_3.diameter                    = _diameter_3_.text
    __MissionOrbitInsertion.stage_3.gross_mass                  = _gross_mass_3_.text
    __MissionOrbitInsertion.stage_3.payload_mass                = _payload_mass_3_.text
    __MissionOrbitInsertion.stage_3.total_mass                  = _total_mass_3_.text

    __MissionOrbitInsertion.payload_mass                        = _payload_mass_.text

    // * Propulsion

    __MissionOrbitInsertion.stage_1.vacuum_specific_impulse     = _specific_impulse_1_.text
    __MissionOrbitInsertion.stage_1.vacuum_thrust               = _thrust_1_.text
    __MissionOrbitInsertion.stage_1.propellant_mass_flow_rate   = _propellant_mass_flow_rate_1_.text
    __MissionOrbitInsertion.stage_1.burn_time                   = _burn_time_1_.text

    __MissionOrbitInsertion.stage_2.vacuum_specific_impulse     = _specific_impulse_2_.text
    __MissionOrbitInsertion.stage_2.vacuum_thrust               = _thrust_2_.text
    __MissionOrbitInsertion.stage_2.propellant_mass_flow_rate   = _propellant_mass_flow_rate_2_.text
    __MissionOrbitInsertion.stage_2.burn_time                   = _burn_time_2_.text

    __MissionOrbitInsertion.stage_3.vacuum_specific_impulse     = _specific_impulse_3_.text
    __MissionOrbitInsertion.stage_3.vacuum_thrust               = _thrust_3_.text
    __MissionOrbitInsertion.stage_3.propellant_mass_flow_rate   = _propellant_mass_flow_rate_3_.text
    __MissionOrbitInsertion.stage_3.burn_time                   = _burn_time_3_.text

    // * Aerodynamics

    __MissionOrbitInsertion.stage_1.drag_coefficient        = _drag_coefficient_1_.text
    __MissionOrbitInsertion.stage_1.lift_coefficient        = _lift_coefficient_1_.text
    __MissionOrbitInsertion.stage_1.reference_surface       = _reference_surface_1_.text

    __MissionOrbitInsertion.stage_2.drag_coefficient        = _drag_coefficient_2_.text
    __MissionOrbitInsertion.stage_2.lift_coefficient        = _lift_coefficient_2_.text
    __MissionOrbitInsertion.stage_2.reference_surface       = _reference_surface_2_.text

    __MissionOrbitInsertion.stage_3.drag_coefficient        = _drag_coefficient_3_.text
    __MissionOrbitInsertion.stage_3.lift_coefficient        = _lift_coefficient_3_.text
    __MissionOrbitInsertion.stage_3.reference_surface       = _reference_surface_3_.text

    // * Connect Stages

    __MissionOrbitInsertion.connect_stages()
}

// >>> Restores the parameters of the dialog.
function restoreParameters()
{   
    // * Structure

    _structural_mass_1_.text            = __MissionOrbitInsertion.stage_1.structural_mass
    _propellant_mass_1_.text            = __MissionOrbitInsertion.stage_1.propellant_mass
    _diameter_1_.text                   = __MissionOrbitInsertion.stage_1.diameter
    _gross_mass_1_.text                 = __MissionOrbitInsertion.stage_1.gross_mass
    _payload_mass_1_.text               = __MissionOrbitInsertion.stage_1.payload_mass
    _total_mass_1_.text                 = __MissionOrbitInsertion.stage_1.total_mass

    _structural_mass_2_.text            = __MissionOrbitInsertion.stage_2.structural_mass
    _propellant_mass_2_.text            = __MissionOrbitInsertion.stage_2.propellant_mass
    _diameter_2_.text                   = __MissionOrbitInsertion.stage_2.diameter
    _gross_mass_2_.text                 = __MissionOrbitInsertion.stage_2.gross_mass
    _payload_mass_2_.text               = __MissionOrbitInsertion.stage_2.payload_mass
    _total_mass_2_.text                 = __MissionOrbitInsertion.stage_2.total_mass

    _structural_mass_3_.text            = __MissionOrbitInsertion.stage_3.structural_mass
    _propellant_mass_3_.text            = __MissionOrbitInsertion.stage_3.propellant_mass
    _diameter_3_.text                   = __MissionOrbitInsertion.stage_3.diameter
    _gross_mass_3_.text                 = __MissionOrbitInsertion.stage_3.gross_mass
    _payload_mass_3_.text               = __MissionOrbitInsertion.stage_3.payload_mass
    _total_mass_3_.text                 = __MissionOrbitInsertion.stage_3.total_mass

    _payload_mass_.text                 = __MissionOrbitInsertion.payload_mass

    // * Propulsion

    _specific_impulse_1_.text           = __MissionOrbitInsertion.stage_1.vacuum_specific_impulse
    _thrust_1_.text                     = __MissionOrbitInsertion.stage_1.vacuum_thrust
    _propellant_mass_flow_rate_1_.text  = __MissionOrbitInsertion.stage_1.propellant_mass_flow_rate
    _burn_time_1_.text                  = __MissionOrbitInsertion.stage_1.burn_time

    _specific_impulse_2_.text           = __MissionOrbitInsertion.stage_2.vacuum_specific_impulse
    _thrust_2_.text                     = __MissionOrbitInsertion.stage_2.vacuum_thrust
    _propellant_mass_flow_rate_2_.text  = __MissionOrbitInsertion.stage_2.propellant_mass_flow_rate
    _burn_time_2_.text                  = __MissionOrbitInsertion.stage_2.burn_time

    _specific_impulse_3_.text           = __MissionOrbitInsertion.stage_3.vacuum_specific_impulse
    _thrust_3_.text                     = __MissionOrbitInsertion.stage_3.vacuum_thrust
    _propellant_mass_flow_rate_3_.text  = __MissionOrbitInsertion.stage_3.propellant_mass_flow_rate
    _burn_time_3_.text                  = __MissionOrbitInsertion.stage_3.burn_time

    // * Aerodynamics

    _drag_coefficient_1_.text           = __MissionOrbitInsertion.stage_1.drag_coefficient
    _lift_coefficient_1_.text           = __MissionOrbitInsertion.stage_1.lift_coefficient
    _reference_surface_1_.text          = __MissionOrbitInsertion.stage_1.reference_surface

    _drag_coefficient_2_.text           = __MissionOrbitInsertion.stage_2.drag_coefficient
    _lift_coefficient_2_.text           = __MissionOrbitInsertion.stage_2.lift_coefficient
    _reference_surface_2_.text          = __MissionOrbitInsertion.stage_2.reference_surface

    _drag_coefficient_3_.text           = __MissionOrbitInsertion.stage_3.drag_coefficient
    _lift_coefficient_3_.text           = __MissionOrbitInsertion.stage_3.lift_coefficient
    _reference_surface_3_.text          = __MissionOrbitInsertion.stage_3.reference_surface
}