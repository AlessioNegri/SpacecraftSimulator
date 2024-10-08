import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "../dialogs/DialogManeuvers.js" as Script

// ? The Maneuver class manages the generic maneuver.
Rectangle
{
    // ? Unique id of the object.
    property int p_Id: 0

    // ? Index of the selected maneuver.
    property int p_Type: 0

    // ? Index of the maneuver's option.
    property int p_Option: 0

    // ? Value of the maneuver's option.
    property string p_OptionValue: ""

    // ? Value of the maneuver's delta velocity.
    property string p_DeltaVelocity: "0.0"

    // ? Value of the maneuver's delta time.
    property string p_DeltaTime: "0.0"

    // ? Value of the maneuver's delta mass.
    property string p_DeltaMass: "0.0"

    // ! ----------------------------------------- ! //

    id: root
    width: parent.width - 20
    height: 100
    color: "transparent"
    border.color: "#FFFFFF"
    border.width: 2
    radius: 5

    RowLayout
    {
        anchors.fill: parent

        Item { width: 10 }

        // ? Maneuver

        ComboBox
        {
            id: _maneuver_
            Material.background: Material.Orange
            implicitWidth: 300
            currentIndex: p_Type

            model:
            [
                "Hohmann Transfer",
                "Bi-Elliptic Hohmann Transfer",
                "Plane Change Maneuver",
                "Apse Line Rotation From Eta"
            ]

            onCurrentIndexChanged:
            {
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

        // ? Option

        ComboBox
        {
            id: _option_
            Material.background: Material.Orange
            implicitWidth: 250
            currentIndex: p_Option
            visible: _maneuver_.currentIndex === 0 || _maneuver_.currentIndex === 1 || _maneuver_.currentIndex === 3
            
            model:
            [
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
            implicitWidth: 200
            placeholderText: "Support Radius"
            onTextEdited: p_OptionValue = text
        }

        TextField
        {
            text: p_DeltaVelocity
            implicitWidth: 125
            placeholderText: "Δv [km / s]"
            readOnly: true
        }

        TextField
        {
            text: p_DeltaTime
            implicitWidth: 125
            placeholderText: "Δt [h]"
            readOnly: true
        }

        TextField
        {
            text: p_DeltaMass
            implicitWidth: 125
            placeholderText: "Δm [kg]"
            readOnly: true
        }

        Item { Layout.fillWidth: true }

        Button
        {
            text: "Remove"
            icon.source: "/images/img/delete.svg"
            font.pointSize: 12
            font.bold: true
            Material.background: "#F44336"
            Material.foreground: "#FFFFFF"
            Layout.alignment: Qt.AlignRight
            onClicked: Script.removeManeuver(p_Id)
        }

        Item { width: 10 }
    }
}