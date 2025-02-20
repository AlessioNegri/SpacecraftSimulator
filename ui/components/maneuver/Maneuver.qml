import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "../../pages/js/PageOrbitTransferLeft.js" as Script

import "../material"

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

    MaterialComboBox
    {
        id: _maneuver_
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

    MaterialComboBox
    {
        id: _option_
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

    MaterialIcon
    {
        source: "/svg/delete.svg"
        baseColor: "#F44336"
        tooltip: "Remove"
        
        function f_Click() { Script.removeManeuver(p_Id) }
    }
}