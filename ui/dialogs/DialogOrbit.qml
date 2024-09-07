import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "../components"

import "DialogOrbit.js" as Script

// ? The DialogOrbit class manages the orbit dialog.
Dialog
{
    // ? Distinguishes between departure and arrival orbit.
    property bool p_Departure: true

    DialogFigure
    {
        id: _orbitPreview_
        title: "Orbit Preview"
        p_FigureCanvasName: p_Departure ? "DepartureOrbitFigure" : "ArrivalOrbitFigure"
        p_FigureCanvasModel: p_Departure ? __DepartureOrbitFigure : __ArrivalOrbitFigure
    }

    DialogFigure
    {
        id: _groundTrackPreview_
        title: "Ground Track Preview"
        p_FigureCanvasName: p_Departure ? "DepartureGroundTrackFigure" : "ArrivalGroundTrackFigure"
        p_FigureCanvasModel: p_Departure ? __DepartureGroundTrackFigure : __ArrivalGroundTrackFigure
    }

    // ! ----------------------------------------- ! //

    id: root
    anchors.centerIn: parent
    modal: true
    width: window.width * 0.8
    height: window.height * 0.8
    closePolicy: Popup.NoAutoClose
    font.pointSize: 12

    onVisibleChanged:
    {
        if (visible)
        {
            p_Departure ? __MissionOrbitTransfer.fill_departure_orbit() : __MissionOrbitTransfer.fill_arrival_orbit()
        }

        Script.restoreParameters()
    }

    header: DialogHeader
    {
        p_Title: p_Departure ? "Departure Orbit" : "Arrival Orbit"
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
            Script.saveParameters()
            
            close()
        }

        function f_Update()
        {
            Script.saveParameters()
        }
    }

    contentItem: Rectangle
    {
        color: "transparent"

        ColumnLayout
        {
            width: parent.width
            spacing: 25

            // --- HEADER 

            RowLayout
            {
                spacing: 10
                Layout.fillWidth: true

                Text
                {
                    text: "Celestial Body"
                    color: "#FFFFFF"
                    font.pointSize: 14
                    Layout.alignment: Qt.AlignCenter
                }

                ComboBox
                {
                    id: _celestial_body_
                    font.pointSize: 12
                    implicitWidth: 150
                    implicitHeight: 50
                    model: [ "SUN", "MERCURY", "VENUS", "EARTH", "MOON", "MARS", "JUPITER", "SATURN", "URANUS", "NEPTUNE", "PLUTO" ]
                }

                Text
                {
                    text: "Representation"
                    color: "#FFFFFF"
                    font.pointSize: 14
                    leftPadding: 20
                    Layout.alignment: Qt.AlignCenter
                }

                ComboBox
                {
                    id: _representation_
                    Material.background: Material.Orange
                    implicitWidth: 200
                    implicitHeight: 50
                    model: [ "Cartesian", "Keplerian", "Modified Keplerian" ]
                }

                Item { Layout.fillWidth: true }

                Button
                {
                    text: "Orbit"
                    font.pointSize: 12
                    font.bold: true
                    Layout.alignment: Qt.AlignRight
                    Material.background: "#009688"
                    Material.foreground: "#FFFFFF"

                    onClicked:
                    {
                        p_Departure ? __MissionOrbitTransfer.evaluate_departure_orbit() : __MissionOrbitTransfer.evaluate_arrival_orbit()
                        
                        _orbitPreview_.open()
                    }
                }

                Button
                {
                    text: "Ground Track"
                    font.pointSize: 12
                    font.bold: true
                    Layout.alignment: Qt.AlignRight
                    Material.background: "#009688"
                    Material.foreground: "#FFFFFF"
                    
                    onClicked:
                    {
                        p_Departure ? __MissionOrbitTransfer.evaluate_departure_ground_track() : __MissionOrbitTransfer.evaluate_arrival_ground_track()
                        
                        _groundTrackPreview_.open()
                    }
                }
            }

            // --- PARAMETERS 

            RowLayout
            {
                spacing: 20
                Layout.fillWidth: true

                ColumnLayout
                {
                    spacing: 20

                    Label
                    {
                        text: "Cartesian"
                        font.bold: true
                        font.pointSize: 16
                        Layout.alignment: Qt.AlignHCenter
                        Layout.columnSpan: 3
                    }

                    DialogParameter
                    {
                        id: _x_
                        placeholderText: "X [km]"
                        enabled: _representation_.currentIndex === 0
                        Layout.fillWidth: true
                    }

                    DialogParameter
                    {
                        id: _y_
                        placeholderText: "Y [km]"
                        enabled: _representation_.currentIndex === 0
                        Layout.fillWidth: true
                    }

                    DialogParameter
                    {
                        id: _z_
                        placeholderText: "Z [km]"
                        enabled: _representation_.currentIndex === 0
                        Layout.fillWidth: true
                    }

                    DialogParameter
                    {
                        id: _v_x_
                        placeholderText: "Vx [km/s]"
                        enabled: _representation_.currentIndex === 0
                        Layout.fillWidth: true
                    }

                    DialogParameter
                    {
                        id: _v_y_
                        placeholderText: "Vy [km/s]"
                        enabled: _representation_.currentIndex === 0
                        Layout.fillWidth: true
                    }

                    DialogParameter
                    {
                        id: _v_z_
                        placeholderText: "Vz [km/s]"
                        enabled: _representation_.currentIndex === 0
                        Layout.fillWidth: true
                    }
                }

                Rectangle
                {
                    width: 3
                    radius: 3
                    color: Material.color(Material.Orange)
                    Layout.fillHeight: true
                }

                ColumnLayout
                {
                    spacing: 20

                    Label
                    {
                        text: "Keplerian"
                        font.bold: true
                        font.pointSize: 16
                        Layout.alignment: Qt.AlignHCenter
                        Layout.columnSpan: 3
                    }

                    DialogParameter
                    {
                        id: _semi_major_axis_
                        placeholderText: "Semi-Major Axis [km]"
                        enabled: _representation_.currentIndex === 1
                        Layout.fillWidth: true
                    }

                    DialogParameter
                    {
                        id: _eccentricity_
                        placeholderText: "Eccentricity"
                        enabled: _representation_.currentIndex === 1
                        Layout.fillWidth: true
                    }

                    DialogParameter
                    {
                        id: _inclination_
                        placeholderText: "Inclination [deg]"
                        enabled: _representation_.currentIndex === 1
                        Layout.fillWidth: true
                    }

                    DialogParameter
                    {
                        id: _raan_
                        placeholderText: "RAAN [deg]"
                        enabled: _representation_.currentIndex === 1
                        Layout.fillWidth: true
                    }

                    DialogParameter
                    {
                        id: _periapsis_anomaly_
                        placeholderText: "Periapsis Anomaly [deg]"
                        enabled: _representation_.currentIndex === 1
                        Layout.fillWidth: true
                    }

                    DialogParameter
                    {
                        id: _true_anomaly_
                        placeholderText: "True Anomaly [deg]"
                        enabled: _representation_.currentIndex === 1
                        Layout.fillWidth: true
                    }
                }

                Rectangle
                {
                    width: 3
                    radius: 3
                    color: Material.color(Material.Orange)
                    Layout.fillHeight: true
                }

                ColumnLayout
                {
                    spacing: 20

                    Label
                    {
                        text: "Modified Keplerian"
                        font.bold: true
                        font.pointSize: 16
                        Layout.alignment: Qt.AlignHCenter
                        Layout.columnSpan: 3
                    }

                    DialogParameter
                    {
                        id: _periapsis_radius_
                        placeholderText: "Periapsis Radius [km]"
                        enabled: _representation_.currentIndex === 2
                        Layout.fillWidth: true
                    }

                    DialogParameter
                    {
                        id: _apoapsis_radius_
                        placeholderText: "Apoapsis Radius [km]"
                        enabled: _representation_.currentIndex === 2
                        Layout.fillWidth: true
                    }

                    DialogParameter
                    {
                        id: _inclination_2_
                        placeholderText: "Inclination [deg]"
                        enabled: _representation_.currentIndex === 2
                        Layout.fillWidth: true
                    }

                    DialogParameter
                    {
                        id: _raan_2_
                        placeholderText: "RAAN [deg]"
                        enabled: _representation_.currentIndex === 2
                        Layout.fillWidth: true
                    }

                    DialogParameter
                    {
                        id: _periapsis_anomaly_2_
                        placeholderText: "Periapsis Anomaly [deg]"
                        enabled: _representation_.currentIndex === 2
                        Layout.fillWidth: true
                    }

                    DialogParameter
                    {
                        id: _true_anomaly_2_
                        placeholderText: "True Anomaly [deg]"
                        enabled: _representation_.currentIndex === 2
                        Layout.fillWidth: true
                    }
                }
            }
        }
    }
}
