import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "DialogOrbit.js" as Script

// ? The DialogOrbit class manages the orbit dialog.
Dialog
{
    // ? Distinguishes between departure and arrival orbit.
    property bool p_Departure: true

    //!-----------------------------------------!//

    anchors.centerIn: parent
    modal: true
    closePolicy: Popup.NoAutoClose
    font.pointSize: 14
    width: 1100
    height: 700

    DialogFigure {
        id: _orbitPreview_
        title: "Orbit Preview"
        p_FigureCanvasName: p_Departure ? "DepartureOrbitFigure" : "ArrivalOrbitFigure"
        p_FigureCanvasModel: p_Departure ? __DepartureOrbitFigure : __ArrivalOrbitFigure
    }

    DialogFigure {
        id: _groundTrackPreview_
        title: "Ground Track Preview"
        p_FigureCanvasName: p_Departure ? "DepartureGroundTrackFigure" : "ArrivalGroundTrackFigure"
        p_FigureCanvasModel: p_Departure ? __DepartureGroundTrackFigure : __ArrivalGroundTrackFigure
    }

    header: Item
    {
        width: parent.width
        height: 75

        RowLayout
        {
            width: parent.width

            Text
            {
                text: title
                padding: 20
                font.pointSize: 24
                font.bold: true
                color: Material.color(Material.Indigo)
            }

            Item { Layout.fillWidth: true }

            ComboBox
            {
                id: _celestialBody_
                font.pointSize: 12
                implicitWidth: 150
                implicitHeight: 50
                model: [ "SUN", "MERCURY", "VENUS", "EARTH", "MOON", "MARS", "JUPITER", "SATURN", "URANUS", "NEPTUNE", "PLUTO" ]
                currentIndex: __Orbit.body
            }

            Item { width: 10 }
        }
    }

    footer: Item
    {
        width: parent.width
        height: 70
        
        RowLayout
        {
            width: parent.width

            Item { width: 10 }

            ComboBox
            {
                id: _selection_
                Material.background: Material.Orange
                implicitWidth: 200
                implicitHeight: 50
                model: [ "Cartesian", "Keplerian", "Modified Keplerian" ]
                onCurrentIndexChanged: __Orbit.state = currentIndex
            }

            Item { Layout.fillWidth: true }

            Button
            {
                text: "Orbit"
                font.pointSize: 12
                font.bold: true
                Layout.alignment: Qt.AlignRight
                Material.background: Material.Orange
                Material.foreground: "#FFFFFF"

                onClicked:
                {
                    p_Departure ? __MissionOrbitTransfer.evaluateDepartureOrbit() : __MissionOrbitTransfer.evaluateArrivalOrbit()
                    
                    _orbitPreview_.open()
                }
            }

            Button
            {
                text: "Ground Track"
                font.pointSize: 12
                font.bold: true
                Layout.alignment: Qt.AlignRight
                Material.background: Material.Orange
                Material.foreground: "#FFFFFF"
                
                onClicked:
                {
                    p_Departure ? __MissionOrbitTransfer.evaluateDepartureOrbit() : __MissionOrbitTransfer.evaluateArrivalOrbit()
                    
                    _groundTrackPreview_.open()
                }
            }

            Item { Layout.fillWidth: true }

            Button
            {
                text: "Update"
                font.pointSize: 12
                font.bold: true
                Layout.alignment: Qt.AlignRight
                Material.background: Material.Indigo
                Material.foreground: "#FFFFFF"
                onClicked: Script.updateParameters(false)
            }

            Button
            {
                text: "Save"
                font.pointSize: 12
                font.bold: true
                Layout.alignment: Qt.AlignRight
                Material.background: Material.Indigo
                Material.foreground: "#FFFFFF"
                onClicked: Script.updateParameters(true)
            }

            Button
            {
                text: "Close"
                font.pointSize: 12
                font.bold: true
                Layout.alignment: Qt.AlignRight
                Material.background: Material.Grey
                Material.foreground: "#FFFFFF"
                onClicked: close()
            }

            Item { width: 10 }
        }
    }

    Row
    {
        spacing: 20

        GridLayout
        {
            columns: 3
            columnSpacing: 20
            rowSpacing: 20

            Label
            {
                text: "Cartesian"
                font.bold: true
                font.pointSize: 14
                Layout.alignment: Qt.AlignHCenter
                Layout.columnSpan: 3
            }

            Label { text: "X"; Layout.alignment: Qt.AlignHCenter }
            
            TextField
            {
                id: _x_
                text: __Orbit.r_x
                enabled: _selection_.currentIndex === 0
                validator: RegularExpressionValidator { regularExpression: /[+-]?([0-9]*[.])?[0-9]+/ }
                implicitWidth: 200
            }

            Label { text: "[km]" }
            
            Label { text: "Y"; Layout.alignment: Qt.AlignHCenter }

            TextField
            {
                id: _y_
                text: __Orbit.r_y
                enabled: _selection_.currentIndex === 0
                validator: RegularExpressionValidator { regularExpression: /[+-]?([0-9]*[.])?[0-9]+/ }
                Layout.fillWidth: true
            }

            Label { text: "[km]" }

            Label { text: "Z"; Layout.alignment: Qt.AlignHCenter }

            TextField
            {
                id: _z_
                text: __Orbit.r_z
                enabled: _selection_.currentIndex === 0
                validator: RegularExpressionValidator { regularExpression: /[+-]?([0-9]*[.])?[0-9]+/ }
                Layout.fillWidth: true
            }

            Label { text: "[km]" }

            Label { text: "Vx"; Layout.alignment: Qt.AlignHCenter }

            TextField
            {
                id: _v_x_
                text: __Orbit.v_x
                enabled: _selection_.currentIndex === 0
                validator: RegularExpressionValidator { regularExpression: /[+-]?([0-9]*[.])?[0-9]+/ }
                Layout.fillWidth: true
            }

            Label { text: "[km / s]" }

            Label { text: "Vy"; Layout.alignment: Qt.AlignHCenter }

            TextField
            {
                id: _v_y_
                text: __Orbit.v_y
                enabled: _selection_.currentIndex === 0
                validator: RegularExpressionValidator { regularExpression: /[+-]?([0-9]*[.])?[0-9]+/ }
                Layout.fillWidth: true
            }

            Label { text: "[km / s]" }

            Label { text: "Vz"; Layout.alignment: Qt.AlignHCenter }

            TextField
            {
                id: _v_z_
                text: __Orbit.v_z
                enabled: _selection_.currentIndex === 0
                validator: RegularExpressionValidator { regularExpression: /[+-]?([0-9]*[.])?[0-9]+/ }
                Layout.fillWidth: true
            }

            Label { text: "[km / s]" }
        }

        Rectangle
        {
            width: 3
            height: parent.height
            color: Material.color(Material.Indigo)
            radius: 1.5
        }

        GridLayout
        {
            columns: 3
            columnSpacing: 20
            rowSpacing: 20

            Label
            {
                text: "Keplerian"
                font.bold: true
                font.pointSize: 14
                Layout.alignment: Qt.AlignHCenter
                Layout.columnSpan: 3
            }

            Label { text: "a"; Layout.alignment: Qt.AlignHCenter }
            
            TextField
            {
                id: _a_
                text: __Orbit.semi_major_axis
                enabled: _selection_.currentIndex === 1
                validator: RegularExpressionValidator { regularExpression: /[+-]?([0-9]*[.])?[0-9]+/ }
                implicitWidth: 200
            }

            Label { text: "[km]" }
            
            Label { text: "e"; Layout.alignment: Qt.AlignHCenter }

            TextField
            {
                id: _e_
                text: __Orbit.eccentricity
                enabled: _selection_.currentIndex === 1
                validator: RegularExpressionValidator { regularExpression: /[+-]?([0-9]*[.])?[0-9]+/ }
                Layout.fillWidth: true
            }

            Label { text: "" }

            Label { text: "i"; Layout.alignment: Qt.AlignHCenter }

            TextField
            {
                id: _i_
                text: __Orbit.inclination
                enabled: _selection_.currentIndex === 1
                validator: RegularExpressionValidator { regularExpression: /[+-]?([0-9]*[.])?[0-9]+/ }
                Layout.fillWidth: true
            }

            Label { text: "[deg]" }

            Label { text: "Ω"; Layout.alignment: Qt.AlignHCenter }

            TextField
            {
                id: _Omega_
                text: __Orbit.right_ascension_ascending_node
                enabled: _selection_.currentIndex === 1
                validator: RegularExpressionValidator { regularExpression: /[+-]?([0-9]*[.])?[0-9]+/ }
                Layout.fillWidth: true
            }

            Label { text: "[deg]" }

            Label { text: "ω"; Layout.alignment: Qt.AlignHCenter }

            TextField
            {
                id: _omega_
                text: __Orbit.periapsis_anomaly
                enabled: _selection_.currentIndex === 1
                validator: RegularExpressionValidator { regularExpression: /[+-]?([0-9]*[.])?[0-9]+/ }
                Layout.fillWidth: true
            }

            Label { text: "[deg]" }

            Label { text: "θ"; Layout.alignment: Qt.AlignHCenter }

            TextField
            {
                id: _theta_
                text: __Orbit.true_anomaly
                enabled: _selection_.currentIndex === 1
                validator: RegularExpressionValidator { regularExpression: /[+-]?([0-9]*[.])?[0-9]+/ }
                Layout.fillWidth: true
            }

            Label { text: "[deg]" }
        }

        Rectangle
        {
            width: 3
            height: parent.height
            color: Material.color(Material.Indigo)
            radius: 1.5
        }

        GridLayout
        {
            columns: 3
            columnSpacing: 20
            rowSpacing: 20

            Label
            {
                text: "Modified Keplerian"
                font.bold: true
                font.pointSize: 14
                Layout.alignment: Qt.AlignHCenter
                Layout.columnSpan: 3
            }

            Label { text: "Rp"; Layout.alignment: Qt.AlignHCenter }
            
            TextField
            {
                id: _r_p_
                text: __Orbit.periapsis_radius
                enabled: _selection_.currentIndex === 2
                validator: RegularExpressionValidator { regularExpression: /[+-]?([0-9]*[.])?[0-9]+/ }
                implicitWidth: 200
            }

            Label { text: "[km]" }
            
            Label { text: "Ra"; Layout.alignment: Qt.AlignHCenter }

            TextField
            {
                id: _r_a_
                text: __Orbit.apoapsis_radius
                enabled: _selection_.currentIndex === 2
                validator: RegularExpressionValidator { regularExpression: /[+-]?([0-9]*[.])?[0-9]+/ }
                Layout.fillWidth: true
            }

            Label { text: "[km]" }

            Label { text: "i"; Layout.alignment: Qt.AlignHCenter }

            TextField
            {
                id: _i_2_
                text: __Orbit.inclination
                enabled: _selection_.currentIndex === 2
                validator: RegularExpressionValidator { regularExpression: /[+-]?([0-9]*[.])?[0-9]+/ }
                Layout.fillWidth: true
            }

            Label { text: "[deg]" }

            Label { text: "Ω"; Layout.alignment: Qt.AlignHCenter }

            TextField
            {
                id: _Omega_2_
                text: __Orbit.right_ascension_ascending_node
                enabled: _selection_.currentIndex === 2
                validator: RegularExpressionValidator { regularExpression: /[+-]?([0-9]*[.])?[0-9]+/ }
                Layout.fillWidth: true
            }

            Label { text: "[deg]" }

            Label { text: "ω"; Layout.alignment: Qt.AlignHCenter }

            TextField
            {
                id: _omega_2_
                text: __Orbit.periapsis_anomaly
                enabled: _selection_.currentIndex === 2
                validator: RegularExpressionValidator { regularExpression: /[+-]?([0-9]*[.])?[0-9]+/ }
                Layout.fillWidth: true
            }

            Label { text: "[deg]" }

            Label { text: "θ"; Layout.alignment: Qt.AlignHCenter }

            TextField
            {
                id: _theta_2_
                text: __Orbit.true_anomaly
                enabled: _selection_.currentIndex === 2
                validator: RegularExpressionValidator { regularExpression: /[+-]?([0-9]*[.])?[0-9]+/ }
                Layout.fillWidth: true
            }

            Label { text: "[deg]" }
        }
    }
}
