import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "main.js" as Script

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

    DialogSpacecraft { id: _dlgSpacecraft_ }

    DialogOrbit { id: _dlgOrbitDeparture_; title: "Departure Orbit"; p_Departure: true }

    DialogOrbit { id: _dlgOrbitArrival_; title: "Arrival Orbit"; p_Departure: false }

    DialogManeuvers { id: _dlgManeuvers_ }

    DialogPorkChopPlot { id: _dlgPorkChopPlot_ }

    DialogInterplanetaryTransfer { id: _dlgInterplanetaryTransfer_ }

    // ? Menu Bar

    menuBar: MenuBar
    {
        Menu
        {
            title: "File"
            
            /*Action { text: "New..."; shortcut: "Ctrl+N" }*/

            /*Action { text: "Open..."; shortcut: "Ctrl+O" }*/

            /*Action { text: "Save"; shortcut: "Ctrl+S" }*/

            MenuSeparator {}

            Action { text: "Exit"; shortcut: "Ctrl+E"; onTriggered: Qt.quit() }
        }

        Menu
        {
            title: "Missions"

            Action
            {
                text: "Spacecraft Properties"
                onTriggered: { /*__MissionParameters.loadSpacecraftProperties();*/ _dlgSpacecraft_.open() }
            }

            Menu
            {
                id: verticalMenu
                title: "Current Mission"
                width: 300

                MenuItem
                {
                    id: _orbitTransferCheckBox_
                    text: "Orbit Transfer"
                    checkable: true
                    checked: true
                    onTriggered: Script.missionChanged(0)
                }
                
                MenuItem
                {
                    id: _orbitalPerturbationsCheckBox_
                    text: "Orbital Perturbations"
                    checkable: true
                    onTriggered: Script.missionChanged(1)
                }
                
                MenuItem
                {
                    id: _interplanetaryTransferCheckBox_
                    text: "Interplanetary Transfer"
                    checkable: true
                    onTriggered: Script.missionChanged(2)
                }
            }

            MenuSeparator {}
            
            Menu
            {
                title: "Orbit Transfer"
                enabled: gp_CurrentMission === 0

                Action { text: "Departure Orbit"; onTriggered: { __MissionOrbitTransfer.fillDepartureOrbit(); _dlgOrbitDeparture_.open() } }

                Action { text: "Arrival Orbit"; onTriggered: { __MissionOrbitTransfer.fillArrivalOrbit(); _dlgOrbitArrival_.open() } }

                Action { text: "Maneuvers"; onTriggered: _dlgManeuvers_.open() }
            }
            
            Action { text: "Orbital Perturbations"; enabled: gp_CurrentMission === 1 }
            
            Menu
            {
                title: "Interplanetary"
                enabled: gp_CurrentMission === 2

                Action { text: "Pork Chop Plot"; onTriggered: _dlgPorkChopPlot_.open() }

                Action { text: "Interplanetary Transfer"; onTriggered: _dlgInterplanetaryTransfer_.open() }
            }
        }
        
        Menu
        {
            title: "Help"

            Action { text: "About"; shortcut: "Ctrl+A"; onTriggered: _dlgAbout_.open() }
        }
    }

    // ? Swipe View

    SwipeView
    {
        id: _view_
        currentIndex: 0
        interactive: false
        anchors.fill: parent

        PageOrbitTransfer { width: window.width; height: window.height }

        PageOrbitalPerturbations { width: window.width; height: window.height }

        PageInterplanetaryTransfer { width: window.width; height: window.height }
    }

    PageIndicator
    {
        id: indicator
        count: _view_.count
        currentIndex: _view_.currentIndex
        anchors.bottom: _view_.bottom
        anchors.horizontalCenter: parent.horizontalCenter
    }
}