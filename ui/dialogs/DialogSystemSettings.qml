import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "common"
import "system/qml"
import "../components/dialog"
import "../components/material"

// * The DialogMissionSettings class manages the mission settings dialog.
Dialog
{
    // * Menu item source icon.
    property int p_CurrentIndex: 0

    // * Loads all the sections.
    function load()
    {
        _section_launcher_.load()

        _section_spacecraft_.load()

        _section_capsule_.load()
    }

    // ! ----------------------------------------- ! //

    id: root
    anchors.centerIn: parent
    modal: true
    width: window.width * 0.8
    height: window.height * 0.8
    closePolicy: Popup.NoAutoClose
    font.pointSize: 12
    onVisibleChanged: if (visible) load()

    Shortcut
    {
        sequence: StandardKey.Cancel
        context: Qt.ApplicationShortcut
        onActivated: close()
    }

    header: DialogHeader
    {
        p_Title: "System Settings"
        p_ShowSaveButton: true
        p_ShowUpdateButton: true

        function f_Close()
        {
            close()
        }

        function f_Save()
        {
            f_Update()

            close()
        }

        function f_Update()
        {
            _section_launcher_.save()

            _section_spacecraft_.save()

            _section_capsule_.save()
        }
    }

    contentItem: Rectangle
    {
        id: _content_
        color: "transparent"

        ScrollView
        {
            id: _menu_scroll_view_
            anchors.top: parent.top
            anchors.left: parent.left
            anchors.bottom: parent.bottom
            width: _menu_.width// + 20
            contentWidth: _menu_.width// + 20
            contentHeight: _menu_.height

            background: Rectangle
            {
                color: "#209e9e9e"
                radius: 10
                border.color: Material.color(Material.Grey)
                border.width: 2
            }

            ScrollBar.vertical: MaterialScrollBar { orientation: Qt.Vertical }

            ColumnLayout
            {
                id: _menu_
                Layout.alignment: Qt.AlignTop
                spacing: 0

                SettingsMenuItem
                {
                    p_Icon: "/png/launcher.png"
                    p_Text: "Launcher"
                    p_Color: Material.color(Material.LightGreen)
                    p_Selected: p_CurrentIndex === 0
                    
                    function f_Click() { p_CurrentIndex = 0 }
                }

                SettingsMenuItem
                {
                    p_Icon: "/png/spacecraft.png"
                    p_Text: "Spacecraft"
                    p_Color: Material.color(Material.LightGreen)
                    p_Selected: p_CurrentIndex === 1
                    
                    function f_Click() { p_CurrentIndex = 1 }
                }

                SettingsMenuItem
                {
                    p_Icon: "/png/capsule.png"
                    p_Text: "Re-Entry Capsule"
                    p_Color: Material.color(Material.LightGreen)
                    p_Selected: p_CurrentIndex === 2
                    
                    function f_Click() { p_CurrentIndex = 2 }
                }
            }
        }

        StackLayout
        {
            id: _stack_layout_
            anchors.top: parent.top
            anchors.right: parent.right
            anchors.bottom: parent.bottom
            width: parent.width - _menu_scroll_view_.width - 20
            currentIndex: p_CurrentIndex

            SectionLauncher
            {
                id: _section_launcher_
            }

            SectionSpacecraft
            {
                id: _section_spacecraft_
            }

            SectionCapsule
            {
                id: _section_capsule_
            }
        }
    }
}