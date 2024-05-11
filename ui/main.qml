import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "dialogs"
import "pages"

ApplicationWindow
{
    // ? Current mission selected.
    property int gp_CurrentMission: 0

    //!-----------------------------------------!//

    id: window
    title: "Spacecraft Simulator"
    visible: true
    visibility: Window.Maximized
    width: 1200
    height: 700

    // ? Dialogs

    DialogAbout { id: _dlgAbout_ }

    DialogOrbit { id: _dlgOrbitDeparture_; title: "Departure Orbit"; p_Departure: true }

    DialogOrbit { id: _dlgOrbitArrival_; title: "Arrival Orbit"; p_Departure: false }

    DialogSpacecraft { id: _dlgSpacecraft_ }

    DialogManeuvers { id: _dlgManeuvers_ }

    // ? Menu Bar

    menuBar: MenuBar
    {
        Menu
        {
            title: "File"
            
            Action { text: "New..."; shortcut: "Ctrl+N" }

            Action { text: "Open..."; shortcut: "Ctrl+O" }

            Action { text: "Save"; shortcut: "Ctrl+S" }

            MenuSeparator {}

            Action { text: "Exit"; shortcut: "Ctrl+E"; onTriggered: Qt.quit() }
        }

        Menu
        {
            title: "Missions"

            Action
            {
                text: "Departure Orbit"
                onTriggered: { __MissionParameters.loadDepartureOrbit(); _dlgOrbitDeparture_.open() }
            }

            Action
            {
                text: "Arrival Orbit"
                onTriggered: { __MissionParameters.loadArrivalOrbit(); _dlgOrbitArrival_.open() }
            }

            Action
            {
                text: "Spacecraft Properties"
                onTriggered: { __MissionParameters.loadSpacecraftProperties(); _dlgSpacecraft_.open() }
            }

            Menu
            {
                title: "Current Mission"
                width: 300

                MenuItem
                {
                    text: "Orbit Transfer"
                    checkable: true
                    checked: gp_CurrentMission === 0
                    onTriggered: gp_CurrentMission = 0
                }
                
                MenuItem
                {
                    text: "Relative Navigation"
                    checkable: true
                    checked: gp_CurrentMission === 1
                    onTriggered: gp_CurrentMission = 1
                }
                
                MenuItem
                {
                    text: "Interplanetary Transfer"
                    checkable: true
                    checked: gp_CurrentMission === 2
                    onTriggered: gp_CurrentMission = 2
                }
            }

            MenuSeparator {}
            
            Menu
            {
                title: "Orbit Transfer"
                enabled: gp_CurrentMission === 0

                Action { text: "Maneuvers"; onTriggered: _dlgManeuvers_.open() }
            }
            
            Action { text: "Relative Navigation"; enabled: gp_CurrentMission === 1 }
            
            Action { text: "Interplanetary Transfer"; enabled: gp_CurrentMission === 2 }
        }
        
        Menu
        {
            title: "Help"

            Action { text: "About"; shortcut: "Ctrl+A"; onTriggered: _dlgAbout_.open() }
        }
    }

    // ? Stack View

    StackView
    {
        id: _stack_
        anchors.fill: parent
        initialItem: _pageOrbitTransfer_
    }

    Component
    {
        id: _pageOrbitTransfer_
        
        PageOrbitTransfer { width: window.width; height: window.height }
    }
}
