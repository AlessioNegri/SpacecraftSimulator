import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "../components/material"
import "../components/figure"
import "../components/page"

// * The PageOrbitPropagation class manages the orbit propagation page.
Page
{
    // ! ----------------------------------------- ! //

    Component.onCompleted: __MissionOrbitPropagation.attach_canvas()
    Component.onDestruction: __MissionOrbitPropagation.detach_canvas()

    //background: Rectangle { color: "#162A35" }
    header: PageHeader { p_Title: "Orbit Propagation"; p_Source: "/png/orbit_propagation.png" }
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

                            function f_Click() { __MissionOrbitPropagation.simulate() }
                        }
                    }

                    Rectangle
                    {
                        height: 3
                        radius: 10
                        color: Material.color(Material.Grey)
                        Layout.fillWidth: true
                        Layout.alignment: Qt.AlignBottom
                    }

                    PageOrbitPropagationLeft
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
                        id: _figure_semi_major_axis_container_
                        height: 450
                        Layout.fillWidth: true

                        Figure
                        {
                            p_ObjectName: "OrbitPropagationFigureSemiMajorAxis"
                            r_Model: __OrbitPropagationFigureSemiMajorAxis
                            r_OriginalParent: _figure_semi_major_axis_container_
                            r_ExpandedParent: _expanded_container_
                            anchors.fill: parent
                        }
                    }

                    Item
                    {
                        id: _figure_eccentricity_container_
                        height: 450
                        Layout.fillWidth: true

                        Figure
                        {
                            p_ObjectName: "OrbitPropagationFigureEccentricity"
                            r_Model: __OrbitPropagationFigureEccentricity
                            r_OriginalParent: _figure_eccentricity_container_
                            r_ExpandedParent: _expanded_container_
                            anchors.fill: parent
                        }
                    }

                    Item
                    {
                        id: _figure_angular_momentum_container_
                        height: 450
                        Layout.fillWidth: true

                        Figure
                        {
                            p_ObjectName: "OrbitPropagationFigureAngularMomentum"
                            r_Model: __OrbitPropagationFigureAngularMomentum
                            r_OriginalParent: _figure_angular_momentum_container_
                            r_ExpandedParent: _expanded_container_
                            anchors.fill: parent
                        }
                    }

                    Item
                    {
                        id: _figure_inclination_container_
                        height: 450
                        Layout.fillWidth: true
                    
                        Figure
                        {
                            p_ObjectName: "OrbitPropagationFigureInclination"
                            r_Model: __OrbitPropagationFigureInclination
                            r_OriginalParent: _figure_inclination_container_
                            r_ExpandedParent: _expanded_container_
                            anchors.fill: parent
                        }
                    }

                    Item
                    {
                        id: _figure_raan_container_
                        height: 450
                        Layout.fillWidth: true

                        Figure
                        {
                            p_ObjectName: "OrbitPropagationFigureRAAN"
                            r_Model: __OrbitPropagationFigureRAAN
                            r_OriginalParent: _figure_raan_container_
                            r_ExpandedParent: _expanded_container_
                            anchors.fill: parent
                        }
                    }

                    Item
                    {
                        id: _figure_periapsis_anomaly_container_
                        height: 450
                        Layout.fillWidth: true

                        Figure
                        {
                            p_ObjectName: "OrbitPropagationFigurePeriapsisAnomaly"
                            r_Model: __OrbitPropagationFigurePeriapsisAnomaly
                            r_OriginalParent: _figure_periapsis_anomaly_container_
                            r_ExpandedParent: _expanded_container_
                            anchors.fill: parent
                        }
                    }
                }
            }
        }
    }
}