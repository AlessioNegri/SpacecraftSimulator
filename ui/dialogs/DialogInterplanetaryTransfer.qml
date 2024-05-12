import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

// ? The DialogInterplanetaryTransfer class manages the interplanetary transfer dialog.
Dialog
{
    // ? Updates the parameters of the interplanetary transfer.
    function saveParameters()
    {
        __MissionParameters.planet_dep          = _planet_dep_.currentIndex
        __MissionParameters.planet_arr          = _planet_arr_.currentIndex
        __MissionParameters.date_dep            = _date_dep_.displayText
        __MissionParameters.date_arr            = _date_arr_.displayText
        __MissionParameters.height_periapse_dep = _height_periapse_dep_.text
        __MissionParameters.height_periapse_arr = _height_periapse_arr_.text
        __MissionParameters.period_arr          = _period_arr_.text

        __MissionParameters.saveInterplanetaryParameters()

        close()
    }

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

        Text
        {
            text: "Interplanetary Transfer"
            padding: 20
            font.pointSize: 24
            font.bold: true
            color: Material.color(Material.Indigo)
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

            Item { Layout.fillWidth: true }

            Button
            {
                text: "Save"
                font.pointSize: 12
                font.bold: true
                Layout.alignment: Qt.AlignRight
                Material.background: Material.Indigo
                Material.foreground: "#FFFFFF"
                onClicked: saveParameters()
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
            
            Label { text: "Departure Planet"; Layout.alignment: Qt.AlignHCenter }
            
            ComboBox
            {
                id: _planet_dep_
                font.pointSize: 12
                implicitWidth: 200
                model: [ "MERCURY", "VENUS", "EARTH", "MARS", "JUPITER", "SATURN", "URANUS", "NEPTUNE", "PLUTO" ]
                currentIndex: __MissionParameters.planet_dep
            }

            Label { text: "" }
            
            Label { text: "Arrival Planet"; Layout.alignment: Qt.AlignHCenter }
            
            ComboBox
            {
                id: _planet_arr_
                font.pointSize: 12
                implicitWidth: 200
                model: [ "MERCURY", "VENUS", "EARTH", "MARS", "JUPITER", "SATURN", "URANUS", "NEPTUNE", "PLUTO" ]
                currentIndex: __MissionParameters.planet_arr
            }

            Label { text: "" }

            Label { text: "Departure Date"; Layout.alignment: Qt.AlignHCenter }
            
            TextField
            {
                id: _date_dep_
                text: __MissionParameters.date_dep
                inputMask: "0000-00-00 00:00:00;0"
                implicitWidth: 200
            }

            Label { text: "" }

            Label { text: "Arrival Date"; Layout.alignment: Qt.AlignHCenter }
                
            TextField
            {
                id: _date_arr_
                text: __MissionParameters.date_arr
                inputMask: "0000-00-00 00:00:00;0"
                implicitWidth: 200
            }

            Label { text: "" }
        }

        GridLayout
        {
            columns: 3
            columnSpacing: 20
            rowSpacing: 20

            Label { text: "Departure Parking Orbit Height"; Layout.alignment: Qt.AlignHCenter }
            
            TextField
            {
                id: _height_periapse_dep_
                text: __MissionParameters.height_periapse_dep
                validator: RegularExpressionValidator { regularExpression: /[+-]?([0-9]*[.])?[0-9]+/ }
                implicitWidth: 200
            }

            Label { text: "[km]" }

            Label { text: "Arrival Rendezvous Orbit Periapse Height"; Layout.alignment: Qt.AlignHCenter }
            
            TextField
            {
                id: _height_periapse_arr_
                text: __MissionParameters.height_periapse_arr
                validator: RegularExpressionValidator { regularExpression: /[+-]?([0-9]*[.])?[0-9]+/ }
                implicitWidth: 200
            }

            Label { text: "[km]" }

            Label { text: "Arrival Rendezvous Orbit Period"; Layout.alignment: Qt.AlignHCenter }
            
            TextField
            {
                id: _period_arr_
                text: __MissionParameters.period_arr
                validator: RegularExpressionValidator { regularExpression: /[+-]?([0-9]*[.])?[0-9]+/ }
                implicitWidth: 200
            }

            Label { text: "[h]" }
        }
    }
}