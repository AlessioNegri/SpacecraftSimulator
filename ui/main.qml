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

    // ? Dialogs

    DialogAbout { id: _dlgAbout_ }

    DialogMissionSettings { id: _dlgMissionSettings_ }

    // ? Menu Bar

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

            Action
            {
                text: "Orbit Insertion"
                enabled: gp_CurrentMission === 0
            }
            
            Action
            {
                text: "Orbit Transfer"
                enabled: gp_CurrentMission === 1
            }
            
            Action
            {
                text: "Orbit Propagation"
                enabled: gp_CurrentMission === 2
            }
            
            Action
            {
                text: "Interplanetary"
                enabled: gp_CurrentMission === 3
            }

            Action
            {
                text: "Atmospheric Entry"
                enabled: gp_CurrentMission === 4
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

        PageOrbitInsertion { width: window.width; height: window.height - _menu_bar_.height }

        PageOrbitTransfer { width: window.width; height: window.height - _menu_bar_.height }

        PageOrbitPropagation { width: window.width; height: window.height - _menu_bar_.height }

        PageInterplanetaryTransfer { width: window.width; height: window.height - _menu_bar_.height }

        PageAtmosphericEntry { width: window.width; height: window.height - _menu_bar_.height }
    }

    /*PageIndicator
    {
        id: _indicator_
        count: _view_.count
        currentIndex: _view_.currentIndex
        anchors.bottom: _view_.bottom
        anchors.horizontalCenter: parent.horizontalCenter
    }*/
}