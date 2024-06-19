import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "DialogPorkChopPlot.js" as Script

// ? The DialogPorkChopPlot class manages the pork chop plot dialog.
Dialog
{
    //!-----------------------------------------!//
    
    anchors.centerIn: parent
    modal: true
    closePolicy: Popup.NoAutoClose
    font.pointSize: 14
    width: 1100
    height: 700

    Component.onCompleted:
    {
        __MissionInterplanetaryTransfer.updateProgressBar.connect(Script.updateProgressBar)
    }

    DialogFigure {
        id: _porkChopPlot_
        title: "Pork Chop Plot"
        p_FigureCanvasName: "PorkChopPlotFigure"
        p_FigureCanvasModel: __PorkChopPlotFigure
    }

    header: Item
    {
        width: parent.width
        height: 75

        Text
        {
            text: "Pork Chop Plot Design"
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

            ProgressBar
            {
                id: _progressBar_
                value: 0
                implicitWidth: 200
                implicitHeight: 32

                background: Rectangle
                {
                    implicitWidth: 200
                    implicitHeight: 35
                    radius: 3
                    color: Material.color(Material.Grey)
                }

                contentItem: Item
                {
                    implicitWidth: 200
                    implicitHeight: 30

                    Rectangle
                    {
                        width: _progressBar_.visualPosition * parent.width
                        height: parent.height
                        radius: 2
                        color: Material.color(Material.Indigo)
                    }

                    Text
                    {
                        text: parseInt(_progressBar_.value * 100) + " %"
                        anchors.centerIn: parent
                        font.bold: true
                        font.pointSize: 12
                        color: "#FFFFFF"
                    }
                }
            }

            Button
            {
                text: "Generate"
                font.pointSize: 12
                font.bold: true
                Layout.alignment: Qt.AlignRight
                Material.background: Material.Orange
                Material.foreground: "#FFFFFF"
                onClicked: Script.updateParameters()
            }

            Button
            {
                text: "Show"
                font.pointSize: 12
                font.bold: true
                Layout.alignment: Qt.AlignRight
                Material.background: Material.Orange
                Material.foreground: "#FFFFFF"
                onClicked: _porkChopPlot_.open()
            }

            Button
            {
                text: "Stop"
                font.pointSize: 12
                font.bold: true
                Layout.alignment: Qt.AlignRight
                Material.background: Material.Red
                Material.foreground: "#FFFFFF"
                onClicked: __MissionInterplanetaryTransfer.stopCalculatePorkChopPlot()
            }

            Item { Layout.fillWidth: true }

            Button
            {
                text: "Save"
                font.pointSize: 12
                font.bold: true
                Layout.alignment: Qt.AlignRight
                Material.background: Material.Indigo
                Material.foreground: "#FFFFFF"
                onClicked: Script.saveParameters()
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
                id: _pcp_planet_dep_
                font.pointSize: 12
                implicitWidth: 200
                model: [ "MERCURY", "VENUS", "EARTH", "MARS", "JUPITER", "SATURN", "URANUS", "NEPTUNE", "PLUTO" ]
                currentIndex: __MissionInterplanetaryTransfer.pcp_planet_dep
            }

            Label { text: "" }
            
            Label { text: "Arrival Planet"; Layout.alignment: Qt.AlignHCenter }
            
            ComboBox
            {
                id: _pcp_planet_arr_
                font.pointSize: 12
                implicitWidth: 200
                model: [ "MERCURY", "VENUS", "EARTH", "MARS", "JUPITER", "SATURN", "URANUS", "NEPTUNE", "PLUTO" ]
                currentIndex: __MissionInterplanetaryTransfer.pcp_planet_arr
            }

            Label { text: "" }

            Label { text: "Launch Window"; Layout.alignment: Qt.AlignHCenter }

            RowLayout
            {
                spacing: 10

                TextField
                {
                    id: _pcp_launch_window_beg_
                    text: __MissionInterplanetaryTransfer.pcp_launch_window_beg
                    inputMask: "0000-00-00;0"
                    implicitWidth: 150
                }

                TextField
                {
                    id: _pcp_launch_window_end_
                    text: __MissionInterplanetaryTransfer.pcp_launch_window_end
                    inputMask: "0000-00-00;0"
                    implicitWidth: 150
                }
            }

            Label { text: "" }

            Label { text: "Arrival Window"; Layout.alignment: Qt.AlignHCenter }

            RowLayout
            {
                spacing: 10

                TextField
                {
                    id: _pcp_arrival_window_beg_
                    text: __MissionInterplanetaryTransfer.pcp_arrival_window_beg
                    inputMask: "0000-00-00;0"
                    implicitWidth: 150
                }

                TextField
                {
                    id: _pcp_arrival_window_end_
                    text: __MissionInterplanetaryTransfer.pcp_arrival_window_end
                    inputMask: "0000-00-00;0"
                    implicitWidth: 150
                }
            }

            Label { text: "" }

            Label { text: "Step [days]"; Layout.alignment: Qt.AlignHCenter }

            TextField
            {
                id: _pcp_step_
                text: __MissionInterplanetaryTransfer.pcp_step
                validator: RegularExpressionValidator { regularExpression: /[0-9]+/ }
                implicitWidth: 150
            }

            Label { text: "" }
        }
    }
}