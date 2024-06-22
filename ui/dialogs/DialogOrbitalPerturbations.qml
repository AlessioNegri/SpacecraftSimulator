import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "DialogOrbitalPerturbations.js" as Script

// ? The DialogOrbitalPerturbations class manages the orbit perturbations dialog.
Dialog
{
    //!-----------------------------------------!//

    anchors.centerIn: parent
    modal: true
    closePolicy: Popup.NoAutoClose
    font.pointSize: 14
    width: 1100
    height: 700

    header: Item
    {
        width: parent.width
        height: 75

        RowLayout
        {
            width: parent.width

            Text
            {
                text: "Orbital Perturbations"
                padding: 20
                font.pointSize: 24
                font.bold: true
                color: Material.color(Material.Indigo)
            }

            Item { Layout.fillWidth: true }

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

            Item { Layout.fillWidth: true }

            Button
            {
                text: "Save"
                font.pointSize: 12
                font.bold: true
                Layout.alignment: Qt.AlignRight
                Material.background: Material.Indigo
                Material.foreground: "#FFFFFF"
                onClicked: { Script.saveParameters(); close() }
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
                text: "Starting Orbital Elements"
                font.bold: true
                font.pointSize: 14
                Layout.alignment: Qt.AlignHCenter
                Layout.columnSpan: 3
            }

            Label { text: "h"; Layout.alignment: Qt.AlignHCenter }
            
            TextField
            {
                id: _h_
                text: __MissionOrbitPropagation.angular_momentum
                validator: RegularExpressionValidator { regularExpression: /[+-]?([0-9]*[.])?[0-9]+/ }
                implicitWidth: 200
            }

            Label { text: "[km^2 / s]" }
            
            Label { text: "e"; Layout.alignment: Qt.AlignHCenter }

            TextField
            {
                id: _e_
                text: __MissionOrbitPropagation.eccentricity
                validator: RegularExpressionValidator { regularExpression: /[+-]?([0-9]*[.])?[0-9]+/ }
                Layout.fillWidth: true
            }

            Label { text: "" }

            Label { text: "i"; Layout.alignment: Qt.AlignHCenter }

            TextField
            {
                id: _i_
                text: __MissionOrbitPropagation.inclination
                validator: RegularExpressionValidator { regularExpression: /[+-]?([0-9]*[.])?[0-9]+/ }
                Layout.fillWidth: true
            }

            Label { text: "[deg]" }

            Label { text: "Ω"; Layout.alignment: Qt.AlignHCenter }

            TextField
            {
                id: _Omega_
                text: __MissionOrbitPropagation.right_ascension_ascending_node
                validator: RegularExpressionValidator { regularExpression: /[+-]?([0-9]*[.])?[0-9]+/ }
                Layout.fillWidth: true
            }

            Label { text: "[deg]" }

            Label { text: "ω"; Layout.alignment: Qt.AlignHCenter }

            TextField
            {
                id: _omega_
                text: __MissionOrbitPropagation.periapsis_anomaly
                validator: RegularExpressionValidator { regularExpression: /[+-]?([0-9]*[.])?[0-9]+/ }
                Layout.fillWidth: true
            }

            Label { text: "[deg]" }

            Label { text: "θ"; Layout.alignment: Qt.AlignHCenter }

            TextField
            {
                id: _theta_
                text: __MissionOrbitPropagation.true_anomaly
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
                text: "Perturbations"
                font.bold: true
                font.pointSize: 14
                Layout.alignment: Qt.AlignHCenter
                Layout.columnSpan: 3
            }

            CheckBox
            {
                id: _drag_
                text: "Drag"
                checked: __MissionOrbitPropagation.drag
            }
            
            TextField
            {
                id: _B_
                text: __MissionOrbitPropagation.drag_ballistic_coefficient
                validator: RegularExpressionValidator { regularExpression: /[+-]?([0-9]*[.])?[0-9]+/ }
                implicitWidth: 200
            }

            Label { text: "Ballistic Coefficient [m^2 / kg]" }
            
            CheckBox
            {
                id: _gravitational_
                text: "Gravitational"
                checked: __MissionOrbitPropagation.gravitational
            }

            Label { text: ""; Layout.columnSpan: 2 }

            CheckBox
            {
                id: _srp_
                text: "SRP"
                checked: __MissionOrbitPropagation.srp
            }
            
            TextField
            {
                id: _B_SRP_
                text: __MissionOrbitPropagation.srp_ballistic_coefficient
                validator: RegularExpressionValidator { regularExpression: /[+-]?([0-9]*[.])?[0-9]+/ }
                implicitWidth: 200
            }

            Label { text: "SRP Ballistic Coefficient [m^2 / kg]" }

            CheckBox
            {
                id: _third_body_
                text: "Third Body"
                checked: __MissionOrbitPropagation.third_body
            }
            
            ComboBox
            {
                id: _third_body_combo_box_
                implicitWidth: 200
                model: [ "MOON", "SUN" ]
                currentIndex: __MissionOrbitPropagation.third_body_choice
            }

            Label { text: "" }

            Label { text: "Start Date"; Layout.alignment: Qt.AlignHCenter }

            TextField
            {
                id: _start_date
                text: __MissionOrbitPropagation.start_date
                inputMask: "0000-00-00 00:00:00;0"
                implicitWidth: 200
            }

            Label { text: "" }

            Label { text: "End Date"; Layout.alignment: Qt.AlignHCenter }

            TextField
            {
                id: _end_date_
                text: __MissionOrbitPropagation.end_date
                inputMask: "0000-00-00 00:00:00;0"
                implicitWidth: 200
            }

            Label { text: "" }
        }
    }
}
