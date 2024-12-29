// ? Updates the parameters of the dialog.
function saveParameters()
{
    __MissionInterplanetaryTransfer.dep_planet              = p_SelectedDeparturePlanet
    __MissionInterplanetaryTransfer.arr_planet              = p_SelectedArrivalPlanet
    __MissionInterplanetaryTransfer.dep_date                = _departure_date_.displayText
    __MissionInterplanetaryTransfer.arr_date                = _arrival_date_.displayText
    __MissionInterplanetaryTransfer.dep_periapsis_height    = _departure_height_.text
    __MissionInterplanetaryTransfer.arr_periapsis_height    = _arrival_height_.text
    __MissionInterplanetaryTransfer.arr_period              = _arrival_period_.text
    __MissionInterplanetaryTransfer.launch_window_beg       = _launch_window_begin_.displayText
    __MissionInterplanetaryTransfer.launch_window_end       = _launch_window_end_.displayText
    __MissionInterplanetaryTransfer.arrival_window_beg      = _arrival_window_begin_.displayText
    __MissionInterplanetaryTransfer.arrival_window_end      = _arrival_window_end_.displayText
    __MissionInterplanetaryTransfer.window_step             = _window_step_.text
}

// ? Restores the parameters of the dialog.
function restoreParameters()
{
    p_SelectedDeparturePlanet   = __MissionInterplanetaryTransfer.dep_planet
    p_SelectedArrivalPlanet     = __MissionInterplanetaryTransfer.arr_planet
    _departure_date_.text       = __MissionInterplanetaryTransfer.dep_date
    _arrival_date_.text         = __MissionInterplanetaryTransfer.arr_date
    _departure_height_.text     = __MissionInterplanetaryTransfer.dep_periapsis_height
    _arrival_height_.text       = __MissionInterplanetaryTransfer.arr_periapsis_height
    _arrival_period_.text       = __MissionInterplanetaryTransfer.arr_period
    _launch_window_begin_.text  = __MissionInterplanetaryTransfer.launch_window_beg
    _launch_window_end_.text    = __MissionInterplanetaryTransfer.launch_window_end
    _arrival_window_begin_.text = __MissionInterplanetaryTransfer.arrival_window_beg
    _arrival_window_end_.text   = __MissionInterplanetaryTransfer.arrival_window_end
    _window_step_.text          = __MissionInterplanetaryTransfer.window_step
}

// ? Function called when the progress bar must be updated.
function updateProgressBar(value)
{
    _progressBar_.value = value
}

// ? Function called when the pork chop plot has been generated.
function notifyFinished(value)
{
    notification_text.text = "Pork Chop Plot Generated"
                                
    notification.start()
}