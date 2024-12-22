import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "common"
import "mission/qml"
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
        _section_orbit_insertion_.load()

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
            _section_orbit_insertion_.save()

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
                    p_Icon: "/png/orbit_insertion.png"
                    p_Text: "Orbit Insertion"
                    p_Color: Material.color(Material.LightBlue)
                    p_Selected: p_CurrentIndex === 0
                    
                    function f_Click() { p_CurrentIndex = 0 }
                }

                SettingsMenuItem
                {
                    p_Icon: "/png/orbit_transfer.png"
                    p_Text: "Orbit Transfer"
                    p_Color: Material.color(Material.LightBlue)
                    p_Selected: p_CurrentIndex === 1
                    
                    function f_Click() { p_CurrentIndex = 1 }
                }

                SettingsMenuItem
                {
                    p_Icon: "/png/orbit_propagation.png"
                    p_Text: "Orbit Propagation"
                    p_Color: Material.color(Material.LightBlue)
                    p_Selected: p_CurrentIndex === 2
                    
                    function f_Click() { p_CurrentIndex = 2 }
                }

                SettingsMenuItem
                {
                    p_Icon: "/png/interplanetary_transfer.png"
                    p_Text: "Interplanetary Transfer"
                    p_Color: Material.color(Material.LightBlue)
                    p_Selected: p_CurrentIndex === 3
                    
                    function f_Click() { p_CurrentIndex = 3 }
                }

                SettingsMenuItem
                {
                    p_Icon: "/png/atmospheric_entry.png"
                    p_Text: "Atmospheric Entry"
                    p_Color: Material.color(Material.LightBlue)
                    p_Selected: p_CurrentIndex === 4
                    
                    function f_Click() { p_CurrentIndex = 4 }
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

            SectionOrbitInsertion
            {
                id: _section_orbit_insertion_
            }

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