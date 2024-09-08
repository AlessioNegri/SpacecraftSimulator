// ? Updates the parameters of the dialog.
function saveParameters()
{
    __MissionInterplanetaryTransfer.dep_planet              = _planet_dep_.currentIndex
    __MissionInterplanetaryTransfer.arr_planet              = _planet_arr_.currentIndex
    __MissionInterplanetaryTransfer.dep_date                = _date_dep_.displayText
    __MissionInterplanetaryTransfer.arr_date                = _date_arr_.displayText
    __MissionInterplanetaryTransfer.dep_periapsis_height    = _height_periapse_dep_.text
    __MissionInterplanetaryTransfer.arr_periapsis_height    = _height_periapse_arr_.text
    __MissionInterplanetaryTransfer.arr_period              = _period_arr_.text
    __MissionInterplanetaryTransfer.launch_window_beg       = _launch_window_beg_.displayText
    __MissionInterplanetaryTransfer.launch_window_end       = _launch_window_end_.displayText
    __MissionInterplanetaryTransfer.arrival_window_beg      = _arrival_window_beg_.displayText
    __MissionInterplanetaryTransfer.arrival_window_end      = _arrival_window_end_.displayText
    __MissionInterplanetaryTransfer.window_step             = _window_step_.text
}

// ? Restores the parameters of the dialog.
function restoreParameters()
{
    _planet_dep_.currentIndex   = __MissionInterplanetaryTransfer.dep_planet
    _planet_arr_.currentIndex   = __MissionInterplanetaryTransfer.arr_planet
    _date_dep_.text             = __MissionInterplanetaryTransfer.dep_date
    _date_arr_.text             = __MissionInterplanetaryTransfer.arr_date
    _height_periapse_dep_.text  = __MissionInterplanetaryTransfer.dep_periapsis_height
    _height_periapse_arr_.text  = __MissionInterplanetaryTransfer.arr_periapsis_height
    _period_arr_.text           = __MissionInterplanetaryTransfer.arr_period
    _launch_window_beg_.text    = __MissionInterplanetaryTransfer.launch_window_beg
    _launch_window_end_.text    = __MissionInterplanetaryTransfer.launch_window_end
    _arrival_window_beg_.text   = __MissionInterplanetaryTransfer.arrival_window_beg
    _arrival_window_end_.text   = __MissionInterplanetaryTransfer.arrival_window_end
    _window_step_.text          = __MissionInterplanetaryTransfer.window_step
}

// ? Function called when the progress bar must be updated.
function updateProgressBar(value)
{
    _progressBar_.value = value
}