import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "../../dialogs/mission/js/SectionOrbitTransfer.js" as Script

// * The Maneuver class manages the generic maneuver.
RowLayout
{
    // * Unique id of the object.
    property int p_Id: 0

    // * Index of the selected maneuver.
    property int p_Type: 0

    // * Index of the maneuver's option.
    property int p_Option: 0

    // * Value of the maneuver's option.
    property string p_OptionValue: ""

    // ! ----------------------------------------- ! //

    id: root
    Layout.fillWidth: true

    ComboBox
    {
        id: _maneuver_
        Material.background: Material.Orange
        implicitWidth: 300
        implicitHeight: 40
        currentIndex: p_Type

        model: [
            "Hohmann Transfer",
            "Bi-Elliptic Hohmann Transfer",
            "Plane Change Maneuver",
            "Apse Line Rotation From Eta"
        ]

        onCurrentIndexChanged: {

            p_Type = currentIndex

            if (currentIndex === 0)
            {
                _option_.model = [ "Periapsis > Apoapsis", "Apoapsis  > Periapsis" ]
            }
            else if (currentIndex === 1)
            {
                _option_.model = [ "Periapsis > Apoapsis" ]
            }
            else if (currentIndex === 3)
            {
                _option_.model = [ "1st Intersection Point", "2nd Intersection Point" ]
            }
        }
    }

    ComboBox
    {
        id: _option_
        Material.background: Material.Orange
        implicitWidth: 250
        implicitHeight: 40
        currentIndex: p_Option
        visible: _maneuver_.currentIndex === 0 || _maneuver_.currentIndex === 1 || _maneuver_.currentIndex === 3
        
        model: [
            "Periapsis > Apoapsis",
            "Apoapsis  > Periapsis"
        ]

        onCurrentIndexChanged: p_Option = currentIndex
    }
    
    TextField
    {
        text: p_OptionValue
        visible: _maneuver_.currentIndex === 1
        validator: RegularExpressionValidator { regularExpression: /[+-]?([0-9]*[.])?[0-9]+/ }
        implicitWidth: 100
        implicitHeight: 40
        placeholderText: "Support Radius"
        onTextEdited: p_OptionValue = text
    }

    Item { Layout.fillWidth: true }

    Button
    {
        icon.source: "/svg/delete.svg"
        font.pointSize: 12
        font.bold: true
        Material.background: "#F44336"
        Material.foreground: "#FFFFFF"
        Layout.alignment: Qt.AlignRight
        onClicked: Script.removeManeuver(p_Id)
    }
}