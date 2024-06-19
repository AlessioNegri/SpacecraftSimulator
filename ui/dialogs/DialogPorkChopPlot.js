// ? Updates the parameters of the pork chop plot.
function saveParameters()
{
    __MissionInterplanetaryTransfer.pcp_planet_dep          = _pcp_planet_dep_.currentIndex
    __MissionInterplanetaryTransfer.pcp_planet_arr          = _pcp_planet_arr_.currentIndex
    __MissionInterplanetaryTransfer.pcp_launch_window_beg   = _pcp_launch_window_beg_.displayText
    __MissionInterplanetaryTransfer.pcp_launch_window_end   = _pcp_launch_window_end_.displayText
    __MissionInterplanetaryTransfer.pcp_arrival_window_beg  = _pcp_arrival_window_beg_.displayText
    __MissionInterplanetaryTransfer.pcp_arrival_window_end  = _pcp_arrival_window_end_.displayText
    __MissionInterplanetaryTransfer.pcp_step                = _pcp_step_.text

    __MissionInterplanetaryTransfer.savePorkChopPlotParameters()

    close()
}

// ? Updates the parameters of the pork chop plot.
function updateParameters()
{
    __MissionInterplanetaryTransfer.pcp_planet_dep          = _pcp_planet_dep_.currentIndex
    __MissionInterplanetaryTransfer.pcp_planet_arr          = _pcp_planet_arr_.currentIndex
    __MissionInterplanetaryTransfer.pcp_launch_window_beg   = _pcp_launch_window_beg_.displayText
    __MissionInterplanetaryTransfer.pcp_launch_window_end   = _pcp_launch_window_end_.displayText
    __MissionInterplanetaryTransfer.pcp_arrival_window_beg  = _pcp_arrival_window_beg_.displayText
    __MissionInterplanetaryTransfer.pcp_arrival_window_end  = _pcp_arrival_window_end_.displayText
    __MissionInterplanetaryTransfer.pcp_step                = _pcp_step_.text

    __MissionInterplanetaryTransfer.calculatePorkChopPlot()
}

function updateProgressBar(value)
{
    _progressBar_.value = value
}