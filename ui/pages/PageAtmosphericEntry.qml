import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "../components/material"
import "../components/figure"
import "../components/page"

// * The PageAtmosphericEntry class manages the atmospheric entry page.
Page
{
    // ! ----------------------------------------- ! //

    Component.onCompleted: __MissionAtmosphericEntry.attach_canvas()
    Component.onDestruction: __MissionAtmosphericEntry.detach_canvas()
    
    background: Rectangle { color: "#162A35" }
    header: PageHeader { p_Title: "Atmospheric Entry"; p_Source: "/png/atmospheric_entry.png" }
    footer: PageFooter {}

    contentItem: Item
    {
        RowLayout
        {
            spacing: 10
            anchors.fill: parent
            anchors.margins: 10

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

                            function f_Click() { __MissionAtmosphericEntry.simulate() }
                        }
                    }

                    Rectangle
                    {
                        height: 3
                        color: Material.color(Material.Grey)
                        Layout.fillWidth: true
                        Layout.alignment: Qt.AlignBottom
                    }

                    PageAtmosphericEntryLeft
                    {
                        id: _section_
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                    }
                }
            }

            ScrollView
            {
                Layout.fillWidth: true
                Layout.fillHeight: true
                contentHeight: _layout_.height

                ScrollBar.vertical: MaterialScrollBar { orientation: Qt.Vertical }
                ScrollBar.horizontal: ScrollBar { policy: ScrollBar.AlwaysOff }

                ColumnLayout
                {
                    id: _layout_
                    width: parent.width - 10
                    spacing: 10

                    Item
                    {
                        id: _figure_velocity_container_
                        height: 450
                        Layout.fillWidth: true

                        Figure
                        {
                            p_ObjectName: "AtmosphericEntryFigureVelocity"
                            r_Model: __AtmosphericEntryFigureVelocity
                            r_OriginalParent: _figure_velocity_container_
                            r_ExpandedParent: _expanded_container_
                            anchors.fill: parent
                        }
                    }

                    Item
                    {
                        id: _figure_acceleration_container_
                        height: 450
                        Layout.fillWidth: true

                        Figure
                        {
                            p_ObjectName: "AtmosphericEntryFigureAcceleration"
                            r_Model: __AtmosphericEntryFigureAcceleration
                            r_OriginalParent: _figure_acceleration_container_
                            r_ExpandedParent: _expanded_container_
                            anchors.fill: parent
                        }
                    }

                    Item
                    {
                        id: _figure_trajectory_container_
                        height: 450
                        Layout.fillWidth: true

                        Figure
                        {
                            p_ObjectName: "AtmosphericEntryFigureTrajectory"
                            r_Model: __AtmosphericEntryFigureTrajectory
                            r_OriginalParent: _figure_trajectory_container_
                            r_ExpandedParent: _expanded_container_
                            anchors.fill: parent
                        }
                    }

                    Item
                    {
                        id: _figure_flight_path_angle_container_
                        height: 450
                        Layout.fillWidth: true
                    
                        Figure
                        {
                            p_ObjectName: "AtmosphericEntryFigureFlightPathAngle"
                            r_Model: __AtmosphericEntryFigureFlightPathAngle
                            r_OriginalParent: _figure_flight_path_angle_container_
                            r_ExpandedParent: _expanded_container_
                            anchors.fill: parent
                        }
                    }

                    Item
                    {
                        id: _figure_convective_heat_flux_container_
                        height: 450
                        Layout.fillWidth: true

                        Figure
                        {
                            p_ObjectName: "AtmosphericEntryFigureConvectiveHeatFlux"
                            r_Model: __AtmosphericEntryFigureConvectiveHeatFlux
                            r_OriginalParent: _figure_convective_heat_flux_container_
                            r_ExpandedParent: _expanded_container_
                            anchors.fill: parent
                        }
                    }

                    Item
                    {
                        id: _figure_altitude_container_
                        height: 450
                        Layout.fillWidth: true

                        Figure
                        {
                            p_ObjectName: "AtmosphericEntryFigureAltitude"
                            r_Model: __AtmosphericEntryFigureAltitude
                            r_OriginalParent: _figure_altitude_container_
                            r_ExpandedParent: _expanded_container_
                            anchors.fill: parent
                        }
                    }
                }
            }
        }
    }
}