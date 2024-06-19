// ? Updates the parameters of the interplanetary transfer.
function saveParameters()
{
    __MissionInterplanetaryTransfer.dep_planet              = _planet_dep_.currentIndex
    __MissionInterplanetaryTransfer.arr_planet              = _planet_arr_.currentIndex
    __MissionInterplanetaryTransfer.dep_date                = _date_dep_.displayText
    __MissionInterplanetaryTransfer.arr_date                = _date_arr_.displayText
    __MissionInterplanetaryTransfer.dep_periapsis_height    = _height_periapse_dep_.text
    __MissionInterplanetaryTransfer.arr_periapsis_height    = _height_periapse_arr_.text
    __MissionInterplanetaryTransfer.arr_period              = _period_arr_.text

    __MissionInterplanetaryTransfer.saveInterplanetaryParameters()
}