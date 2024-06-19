// ? Updates the parameters of the spacecraft.
function saveParameters()
{
    __Spacecraft.initial_mass        = _m_0_.text
    __Spacecraft.specific_impulse    = _I_sp_.text
    __Spacecraft.thrust              = _T_.text
}