import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "js/PageOrbitTransfer.js" as Script

import "../components/material"
import "../components/figure"
import "../components/page"
import "../dialogs"

// * The PageOrbitTransfer class manages the orbit transfer page.
Page
{
    // ! ----------------------------------------- ! //

    Component.onCompleted: { __MissionOrbitTransfer.attach_canvas(); Script.loadManeuvers() }
    Component.onDestruction: __MissionOrbitTransfer.detach_canvas()

    background: Rectangle { color: "#162A35" }
    header: PageHeader { p_Title: "Orbit Transfer"; p_Source: "/png/orbit_transfer.png" }

    DialogFigure
    {
        id: _departure_orbit_preview_
        title: "Departure Orbit Preview"
        p_FigureCanvasName: "DepartureOrbitFigure"
        p_FigureCanvasModel: __DepartureOrbitFigure
    }

    DialogFigure
    {
        id: _departure_ground_track_preview_
        title: "Departure Ground Track Preview"
        p_FigureCanvasName: "DepartureGroundTrackFigure"
        p_FigureCanvasModel: __DepartureGroundTrackFigure
    }

    DialogFigure
    {
        id: _arrival_orbit_preview_
        title: "Arrival Orbit Preview"
        p_FigureCanvasName: "ArrivalOrbitFigure"
        p_FigureCanvasModel: __ArrivalOrbitFigure
    }

    DialogFigure
    {
        id: _arrival_ground_track_preview_
        title: "Arrival Ground Track Preview"
        p_FigureCanvasName: "ArrivalGroundTrackFigure"
        p_FigureCanvasModel: __ArrivalGroundTrackFigure
    }

    contentItem: Item
    {
        GridLayout
        {
            rows: 2
            columns: 2
            rowSpacing: 10
            columnSpacing: 10
            uniformCellHeights: true
            uniformCellWidths: true
            anchors.fill: parent
            anchors.margins: 10

            PageBox
            {
                Layout.rowSpan: 2
                Layout.fillWidth: true
                Layout.fillHeight: true

                ColumnLayout
                {
                    anchors.fill: parent
                    anchors.margins: 10

                    RowLayout
                    {
                        Layout.fillWidth: true
                        spacing: 10

                        Text
                        {
                            text: "Parameters"
                            font.pointSize: 20
                            font.bold: true
                            color: "#93F9D8"
                        }

                        Item
                        {
                            Layout.fillWidth: true
                        }

                        MaterialIcon
                        {
                            source: "/svg/save.svg"
                            tooltip: "Save"
                            tooltipLocation: Qt.AlignTop

                            function f_Click()
                            {
                                _section_.save()

                                notification_text.text = "Parameters Saved"
                                
                                notification.start()
                            }
                        }

                        MaterialIcon
                        {
                            source: "/svg/play_arrow.svg"
                            baseColor: "#00FF00"
                            tooltip: "Simulate"
                            tooltipLocation: Qt.AlignTop

                            function f_Click()
                            {
                                __MissionOrbitTransfer.simulate()

                                Script.loadManeuvers()
                            }
                        }
                    }

                    Rectangle
                    {
                        height: 3
                        color: Material.color(Material.Grey)
                        Layout.fillWidth: true
                        Layout.alignment: Qt.AlignBottom
                    }

                    PageOrbitTransferLeft
                    {
                        id: _section_
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                    }
                }
            }

            Item
            {
                id: _figure_container_
                Layout.fillWidth: true
                Layout.fillHeight: true

                Figure
                {
                    p_ObjectName: "OrbitTransferFigure"
                    r_Model: __OrbitTransferFigure
                    r_OriginalParent: _figure_container_
                    r_ExpandedParent: _expanded_container_
                    anchors.fill: parent
                }
            }

            PageBox
            {
                Layout.fillWidth: true
                Layout.fillHeight: true

                ColumnLayout
                {
                    anchors.fill: parent
                    anchors.margins: 10

                    RowLayout
                    {
                        Layout.fillWidth: true
                        Layout.alignment: Qt.AlignTop
                        spacing: 10

                        Text
                        {
                            text: "Maneuvers"
                            font.pointSize: 20
                            font.bold: true
                            color: "#93F9D8"
                        }
                    }

                    Rectangle
                    {
                        height: 3
                        color: Material.color(Material.Grey)
                        Layout.fillWidth: true
                        Layout.alignment: Qt.AlignTop
                    }

                    ScrollView
                    {
                        width: parent.width
                        contentWidth: parent.width
                        contentHeight: _container_.height
                        Layout.fillHeight: true

                        ScrollBar.vertical: MaterialScrollBar { orientation: Qt.Vertical }
                        ScrollBar.horizontal: ScrollBar { policy: ScrollBar.AlwaysOff }

                        ColumnLayout
                        {
                            id: _container_
                            spacing: 20
                            width: parent.width
                        }
                    }
                }
            }
        }
    }
}