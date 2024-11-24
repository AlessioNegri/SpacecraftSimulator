import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "sections/qml"

import "../components"

// * The DialogSpacecraft class manages the spacecraft dialog.
Dialog
{
    // * Menu item source icon.
    property int p_CurrentIndex: 1

    // * Loads all the sections.
    function load()
    {
        _section_spacecraft_.load()

        _section_capsule_.load()

        _section_orbit_transfer_.load()

        _section_orbit_propagation_.load()

        _section_interplanetary_transfer_.load()

        _section_atmospheric_entry_.load()
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
        p_Title: "Mission Settings"
    }

    footer: DialogFooter
    {
        p_ShowUpdateButton: true

        function f_Close()
        {
            close()
        }

        function f_Save()
        {
            _section_spacecraft_.save()

            _section_capsule_.save()

            _section_orbit_transfer_.save()

            _section_orbit_propagation_.save()

            _section_interplanetary_transfer_.save()

            _section_atmospheric_entry_.save()

            close()
        }

        function f_Update()
        {
            _section_spacecraft_.save()

            _section_capsule_.save()

            _section_orbit_transfer_.save()

            _section_orbit_propagation_.save()

            _section_interplanetary_transfer_.save()

            _section_atmospheric_entry_.save()
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
            width: _menu_.width + 20
            contentWidth: _menu_.width + 20
            contentHeight: _menu_.height

            ColumnLayout
            {
                id: _menu_
                Layout.alignment: Qt.AlignTop
                spacing: 0

                SettingsMenuItem
                {
                    p_Icon: "/png/launcher.png"
                    p_Text: "Launcher"
                    p_Selected: p_CurrentIndex === 0
                    
                    function f_Click() { p_CurrentIndex = 0 }
                }

                SettingsMenuItem
                {
                    p_Icon: "/png/spacecraft.png"
                    p_Text: "Spacecraft"
                    p_Selected: p_CurrentIndex === 1
                    
                    function f_Click() { p_CurrentIndex = 1 }
                }

                SettingsMenuItem
                {
                    p_Icon: "/png/capsule.png"
                    p_Text: "Re-Entry Capsule"
                    p_Selected: p_CurrentIndex === 2
                    
                    function f_Click() { p_CurrentIndex = 2 }
                }

                SettingsMenuItem
                {
                    p_Icon: "/png/orbit_insertion.png"
                    p_Text: "Orbit Insertion"
                    p_MissionType: true
                    p_Selected: p_CurrentIndex === 3
                    
                    function f_Click() { p_CurrentIndex = 3 }
                }

                SettingsMenuItem
                {
                    p_Icon: "/png/orbit_transfer.png"
                    p_Text: "Orbit Transfer"
                    p_MissionType: true
                    p_Selected: p_CurrentIndex === 4
                    
                    function f_Click() { p_CurrentIndex = 4 }
                }

                SettingsMenuItem
                {
                    p_Icon: "/png/orbit_propagation.png"
                    p_Text: "Orbit Propagation"
                    p_MissionType: true
                    p_Selected: p_CurrentIndex === 5
                    
                    function f_Click() { p_CurrentIndex = 5 }
                }

                SettingsMenuItem
                {
                    p_Icon: "/png/interplanetary_transfer.png"
                    p_Text: "Interplanetary Transfer"
                    p_MissionType: true
                    p_Selected: p_CurrentIndex === 6
                    
                    function f_Click() { p_CurrentIndex = 6 }
                }

                SettingsMenuItem
                {
                    p_Icon: "/png/atmospheric_entry.png"
                    p_Text: "Atmospheric Entry"
                    p_MissionType: true
                    p_Selected: p_CurrentIndex === 7
                    
                    function f_Click() { p_CurrentIndex = 7 }
                }
            }
        }

        StackLayout
        {
            id: _stack_layout_
            anchors.top: parent.top
            anchors.right: parent.right
            anchors.bottom: parent.bottom
            width: parent.width - _menu_scroll_view_.width
            currentIndex: p_CurrentIndex

            Item {}

            SectionSpacecraft
            {
                id: _section_spacecraft_
            }

            SectionCapsule
            {
                id: _section_capsule_
            }

            Item {}

            SectionOrbitTransfer
            {
                id: _section_orbit_transfer_
            }

            SectionOrbitPropagation
            {
                id: _section_orbit_propagation_
            }

            SectionInterplanetaryTransfer
            {
                id: _section_interplanetary_transfer_
            }

            SectionAtmosphericEntry
            {
                id: _section_atmospheric_entry_
            }
        }
    }

    DialogFigure
    {
        id: _departureOrbitPreview_
        title: "Departure Orbit Preview"
        p_FigureCanvasName: "DepartureOrbitFigure"
        p_FigureCanvasModel: __DepartureOrbitFigure
    }

    DialogFigure
    {
        id: _departureGroundTrackPreview_
        title: "Departure Ground Track Preview"
        p_FigureCanvasName: "DepartureGroundTrackFigure"
        p_FigureCanvasModel: __DepartureGroundTrackFigure
    }

    DialogFigure
    {
        id: _arrivalOrbitPreview_
        title: "Arrival Orbit Preview"
        p_FigureCanvasName: "ArrivalOrbitFigure"
        p_FigureCanvasModel: __ArrivalOrbitFigure
    }

    DialogFigure
    {
        id: _arrivalGroundTrackPreview_
        title: "Arrival Ground Track Preview"
        p_FigureCanvasName: "ArrivalGroundTrackFigure"
        p_FigureCanvasModel: __ArrivalGroundTrackFigure
    }

    DialogFigure
    {
        id: _porkChopPlot_
        title: "Pork Chop Plot"
        p_FigureCanvasName: "PorkChopPlotFigure"
        p_FigureCanvasModel: __PorkChopPlotFigure
    }
}