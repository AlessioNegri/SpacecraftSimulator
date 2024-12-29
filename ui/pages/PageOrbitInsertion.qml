import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "../components/material"
import "../components/figure"
import "../components/page"

// * The PageOrtbitInsertion class manages the orbit insertion page.
Page
{
    // ! ----------------------------------------- ! //
    
    Component.onCompleted: __MissionOrbitInsertion.attach_canvas()
    Component.onDestruction: __MissionOrbitInsertion.detach_canvas()

    background: Rectangle { color: "#162A35" }
    header: PageHeader { p_Title: "Orbit Insertion"; p_Source: "/png/orbit_insertion.png" }

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

                            function f_Click() { __MissionOrbitInsertion.simulate() }
                        }
                    }

                    Rectangle
                    {
                        height: 3
                        color: Material.color(Material.Grey)
                        Layout.fillWidth: true
                        Layout.alignment: Qt.AlignBottom
                    }

                    PageOrbitInsertionLeft
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
                            p_ObjectName: "OrbitInsertionFigureVelocity"
                            r_Model: __OrbitInsertionFigureVelocity
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
                            p_ObjectName: "OrbitInsertionFigureAcceleration"
                            r_Model: __OrbitInsertionFigureAcceleration
                            r_OriginalParent: _figure_acceleration_container_
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
                            p_ObjectName: "OrbitInsertionFigureFlightPathAngle"
                            r_Model: __OrbitInsertionFigureFlightPathAngle
                            r_OriginalParent: _figure_flight_path_angle_container_
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
                            p_ObjectName: "OrbitInsertionFigureTrajectory"
                            r_Model: __OrbitInsertionFigureTrajectory
                            r_OriginalParent: _figure_trajectory_container_
                            r_ExpandedParent: _expanded_container_
                            anchors.fill: parent
                        }
                    }
                }
            }
        }
    }
}