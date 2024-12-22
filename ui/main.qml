import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "main.js" as Script

import "dialogs"
import "pages/qml"

// * Main window application
ApplicationWindow
{
    // * Current mission selected.
    property int gp_CurrentMission: 0

    // ! ----------------------------------------- ! //

    id: window
    title: "Spacecraft Simulator"
    visible: true
    visibility: Window.Maximized
    width: 1200
    height: 700

    Component.onCompleted:
    {
        console.log("Info")
        console.warn("Warning")
        console.error("Error")
    }

    // * Dialogs

    DialogAbout { id: _dlgAbout_ }

    DialogSystemSettings { id: _dlgSystemSettings_ }

    DialogMissionSettings { id: _dlgMissionSettings_ }

    // * Menu Bar

    menuBar: MenuBar
    {
        id: _menu_bar_

        Menu
        {
            title: "File"

            MenuSeparator {}

            Action
            {
                text: "Exit"
                shortcut: "Ctrl+E"
                onTriggered: Qt.quit()
            }
        }

        Menu
        {
            title: "Edit"

            Action
            {
                text: "System Settings"
                shortcut: "Ctrl+S"
                onTriggered: _dlgSystemSettings_.open()
            }

            Action
            {
                text: "Mission Settings"
                shortcut: "Ctrl+M"
                onTriggered: _dlgMissionSettings_.open()
            }
        }

        Menu
        {
            title: "Missions"

            Menu
            {
                id: verticalMenu
                title: "Current Mission"
                width: 300

                MenuItem
                {
                    id: _orbitInsertionCheckBox_
                    text: "Orbit Insertion"
                    checkable: true
                    checked: true
                    onTriggered: Script.missionChanged(0)
                }

                MenuItem
                {
                    id: _orbitTransferCheckBox_
                    text: "Orbit Transfer"
                    checkable: true
                    onTriggered: Script.missionChanged(1)
                }
                
                MenuItem
                {
                    id: _orbitPropagationCheckBox_
                    text: "Orbit Propagation"
                    checkable: true
                    onTriggered: Script.missionChanged(2)
                }
                
                MenuItem
                {
                    id: _interplanetaryTransferCheckBox_
                    text: "Interplanetary Transfer"
                    checkable: true
                    onTriggered: Script.missionChanged(3)
                }

                MenuItem
                {
                    id: _atmosphericEntryCheckBox_
                    text: "Atmospheric Entry"
                    checkable: true
                    onTriggered: Script.missionChanged(4)
                }
            }

            MenuSeparator {}

            Menu
            {
                title: "Orbit Insertion"
                enabled: gp_CurrentMission === 0

                MenuItem
                {
                    text: "Simulation"
                    icon.name: "sim"
                    icon.source: "/svg/play_arrow.svg"
                    onTriggered: __MissionOrbitInsertion.simulate()
                }
            }
            
            Menu
            {
                title: "Orbit Transfer"
                enabled: gp_CurrentMission === 1

                MenuItem
                {
                    text: "Simulation"
                    icon.name: "sim"
                    icon.source: "/svg/play_arrow.svg"
                    onTriggered: {__MissionOrbitTransfer.simulate(); _page_orbit_transfer_.update() }
                }
            }
            
            Menu
            {
                title: "Orbit Propagation"
                enabled: gp_CurrentMission === 2

                MenuItem
                {
                    text: "Simulation"
                    icon.name: "sim"
                    icon.source: "/svg/play_arrow.svg"
                    onTriggered: __MissionOrbitPropagation.simulate()
                }
            }
            
            Menu
            {
                title: "Interplanetary"
                enabled: gp_CurrentMission === 3

                MenuItem
                {
                    text: "Simulation"
                    icon.name: "sim"
                    icon.source: "/svg/play_arrow.svg"
                    onTriggered: __MissionInterplanetaryTransfer.simulate()
                }
            }

            Menu
            {
                title: "Atmospheric Entry"
                enabled: gp_CurrentMission === 4

                MenuItem
                {
                    text: "Simulation"
                    icon.name: "sim"
                    icon.source: "/svg/play_arrow.svg"
                    onTriggered: __MissionAtmosphericEntry.simulate()
                }
            }
        }
        
        Menu
        {
            title: "Help"

            Action { text: "About"; shortcut: "Ctrl+A"; onTriggered: _dlgAbout_.open() }
        }
    }

    // * Swipe View

    SwipeView
    {
        id: _view_
        currentIndex: 0
        interactive: false
        anchors.fill: parent

        PageOrbitInsertion { id: _page_orbit_insertion_; width: window.width; height: window.height - _menu_bar_.height }

        PageOrbitTransfer { id: _page_orbit_transfer_; width: window.width; height: window.height - _menu_bar_.height }

        PageOrbitPropagation { id: _page_orbit_propagation_; width: window.width; height: window.height - _menu_bar_.height }

        PageInterplanetaryTransfer { id: _page_interplanetary_trensfer_; width: window.width; height: window.height - _menu_bar_.height }

        PageAtmosphericEntry { id: _page_atmospheric_entry_; width: window.width; height: window.height - _menu_bar_.height }
    }
}