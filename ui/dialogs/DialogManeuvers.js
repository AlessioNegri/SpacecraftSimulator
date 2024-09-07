// ? Clears the maneuvers.
function clearManeuvers()
{
    for (let i = r_Maneuvers.length - 1; i >= 0; --i)
    {
        r_Maneuvers[i].destroy()

        r_Maneuvers.pop()
    }

    _scrollView_.contentHeight = (100 + 16) * (r_Maneuvers.length)
}

// ? Loads the maneuvers from the backend.
function loadManeuvers()
{
    // * Clear

    clearManeuvers()

    // * Cycle

    let len = __MissionOrbitTransfer.maneuver_count()

    for (let i = 0; i < len; ++i)
    {
        // * Retrieve maneuver from backend

        var maneuver = __MissionOrbitTransfer.maneuver(i)

        // * Create QML component

        let component = Qt.createComponent("../components/Maneuver.qml")

        if (component.status == Component.Ready)
        {
            var obj = component.createObject(_container_,
            {
                "p_Id"              : r_Maneuvers.length + 1,
                "p_Type"            : maneuver.type,
                "p_Option"          : maneuver.option,
                "p_OptionValue"     : maneuver.option_value,
                "p_DeltaVelocity"   : maneuver.delta_velocity,
                "p_DeltaTime"       : maneuver.delta_time,
                "p_DeltaMass"       : maneuver.delta_mass
            })
            
            if (obj == null)
            {
                console.log("Error creating object")

                continue
            }

            // * Add and update

            r_Maneuvers.push(obj)

            _scrollView_.contentHeight = (100 + 16) * (r_Maneuvers.length)
        }
        else if (component.status == Component.Error)
        {
            console.log("Error loading component:" + component.errorString())
        }
    }
}

// ? Adds a new maneuver.
function addManeuver()
{
    // * Create QML component

    let component = Qt.createComponent("../components/Maneuver.qml")

    if (component.status == Component.Ready)
    {
        var obj = component.createObject(_container_, { "p_Id": r_Maneuvers.length + 1 })
        
        if (obj == null)
        {
            console.log("Error creating object")
        }

        // * Add and update

        r_Maneuvers.push(obj)

        _scrollView_.contentHeight = (100 + 16) * (r_Maneuvers.length)
    }
    else if (component.status == Component.Error)
    {
        console.log("Error loading component:" + component.errorString())
    }
}

// ? Removes the maneuvers with the given Id.
function removeManeuver(id)
{
    for (let i = 0; i < r_Maneuvers.length; ++i)
    {
        if (r_Maneuvers[i].p_Id === id)
        {
            r_Maneuvers[i].destroy()

            r_Maneuvers.splice(i, 1)

            _scrollView_.contentHeight = (100 + 16) * (r_Maneuvers.length)

            break
        }
    }
}

// ? Updates the maneuvers in the backend.
function saveManeuvers()
{
    __MissionOrbitTransfer.clear_maneuvers()

    for (let i = 0; i < r_Maneuvers.length; ++i)
    {
        __MissionOrbitTransfer.add_maneuver(r_Maneuvers[i].p_Type, r_Maneuvers[i].p_Option, r_Maneuvers[i].p_OptionValue)
    }

    //__MissionOrbitTransfer.saveManeuvers()

    close()
}