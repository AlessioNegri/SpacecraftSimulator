import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "../components"

import "DialogInterplanetaryTransfer.js" as Script

// ? The DialogInterplanetaryTransfer class manages the interplanetary transfer dialog.
Dialog
{
    DialogFigure
    {
        id: _porkChopPlot_
        title: "Pork Chop Plot"
        p_FigureCanvasName: "PorkChopPlotFigure"
        p_FigureCanvasModel: __PorkChopPlotFigure
    }

    // ! ----------------------------------------- ! //
    
    id: root
    anchors.centerIn: parent
    modal: true
    width: window.width * 0.8
    height: window.height * 0.8
    closePolicy: Popup.NoAutoClose
    font.pointSize: 12

    Component.onCompleted: __MissionInterplanetaryTransfer.signal_update_progress_bar.connect(Script.updateProgressBar)

    onVisibleChanged: if (visible) Script.restoreParameters()

    header: DialogHeader
    {
        p_Title: "Interplanetary Transfer"
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

            // --- PLANETS 

            Text
            {
                text: "Planets"
                color: "#FFFFFF"
                font.pointSize: 16
                Layout.fillWidth: true
                Layout.alignment: Qt.AlignHCenter | Qt.AlignTop
            }

            RowLayout
            {
                spacing: 50
                Layout.fillWidth: true
                Layout.alignment: Qt.AlignHCenter | Qt.AlignTop

                Text
                {
                    text: "Departure Planet"
                    color: "#FFFFFF"
                    font.pointSize: 14
                    Layout.alignment: Qt.AlignCenter
                }

                ComboBox
                {
                    id: _planet_dep_
                    font.pointSize: 12
                    implicitWidth: 150
                    implicitHeight: 50
                    model: [ "MERCURY", "VENUS", "EARTH", "MARS", "JUPITER", "SATURN", "URANUS", "NEPTUNE", "PLUTO" ]
                }

                Text
                {
                    text: "Arrival Planet"
                    color: "#FFFFFF"
                    font.pointSize: 14
                    Layout.alignment: Qt.AlignCenter
                }

                ComboBox
                {
                    id: _planet_arr_
                    font.pointSize: 12
                    implicitWidth: 150
                    implicitHeight: 50
                    model: [ "MERCURY", "VENUS", "EARTH", "MARS", "JUPITER", "SATURN", "URANUS", "NEPTUNE", "PLUTO" ]
                }
            }

            Rectangle
            {
                height: 3
                radius: 3
                color: Material.color(Material.Orange)
                Layout.fillWidth: true
            }

            // --- DATES 

            Text
            {
                text: "Dates"
                color: "#FFFFFF"
                font.pointSize: 16
                Layout.fillWidth: true
                Layout.alignment: Qt.AlignHCenter | Qt.AlignTop
            }

            RowLayout
            {
                spacing: 50
                Layout.fillWidth: true
                Layout.alignment: Qt.AlignHCenter | Qt.AlignTop

                DialogParameter
                {
                    id: _launch_window_beg_
                    placeholderText: "Launch Window Begin"
                    inputMask: "0000-00-00;0"
                    p_FloatRegex: false
                    Layout.fillWidth: true
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignTop
                }

                DialogParameter
                {
                    id: _launch_window_end_
                    placeholderText: "Launch Window End"
                    inputMask: "0000-00-00;0"
                    p_FloatRegex: false
                    Layout.fillWidth: true
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignTop
                }

                DialogParameter
                {
                    id: _date_dep_
                    placeholderText: "Departure Date"
                    inputMask: "0000-00-00 00:00:00;0"
                    p_FloatRegex: false
                    Layout.fillWidth: true
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignTop
                }

                DialogParameter
                {
                    id: _arrival_window_beg_
                    placeholderText: "Arrival Window Begin"
                    inputMask: "0000-00-00;0"
                    p_FloatRegex: false
                    Layout.fillWidth: true
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignTop
                }

                DialogParameter
                {
                    id: _arrival_window_end_
                    placeholderText: "Arrival Window End"
                    inputMask: "0000-00-00;0"
                    p_FloatRegex: false
                    Layout.fillWidth: true
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignTop
                }

                DialogParameter
                {
                    id: _date_arr_
                    placeholderText: "Arrival Date"
                    inputMask: "0000-00-00 00:00:00;0"
                    p_FloatRegex: false
                    Layout.fillWidth: true
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignTop
                }
            }

            Rectangle
            {
                height: 3
                radius: 3
                color: Material.color(Material.Orange)
                Layout.fillWidth: true
            }

            // --- PORK CHOP PLOT 

            Text
            {
                text: "Pork Chop Plot"
                color: "#FFFFFF"
                font.pointSize: 16
                Layout.fillWidth: true
                Layout.alignment: Qt.AlignHCenter | Qt.AlignTop
            }

            RowLayout
            {
                spacing: 50
                Layout.fillWidth: true
                Layout.alignment: Qt.AlignHCenter | Qt.AlignTop

                DialogParameter
                {
                    id: _window_step_
                    placeholderText: "Window Step"
                    p_IntRegex: true
                }

                Button
                {
                    text: "Show"
                    font.pointSize: 12
                    font.bold: true
                    Material.background: "#009688"
                    Material.foreground: "#FFFFFF"
                    onClicked: _porkChopPlot_.open()
                }

                Button
                {
                    text: "Generate"
                    font.pointSize: 12
                    font.bold: true
                    Material.background: "#009688"
                    Material.foreground: "#FFFFFF"
                    onClicked: __MissionInterplanetaryTransfer.generate_pork_chop_plot()
                }

                Button
                {
                    text: "Stop"
                    font.pointSize: 12
                    font.bold: true
                    Material.background: "#009688"
                    Material.foreground: "#FFFFFF"
                    onClicked: __MissionInterplanetaryTransfer.stop_generate_pork_chop_plot()
                }

                MaterialProgressBar
                {
                    id: _progressBar_
                    Layout.fillWidth: true
                }
            }

            Rectangle
            {
                height: 3
                radius: 3
                color: Material.color(Material.Orange)
                Layout.fillWidth: true
            }

            // --- ORBITS 

            Text
            {
                text: "Orbits"
                color: "#FFFFFF"
                font.pointSize: 16
                Layout.fillWidth: true
                Layout.alignment: Qt.AlignHCenter | Qt.AlignTop
            }

            RowLayout
            {
                spacing: 50
                Layout.fillWidth: true
                Layout.alignment: Qt.AlignHCenter | Qt.AlignTop

                DialogParameter
                {
                    id: _height_periapse_dep_
                    placeholderText: "Departure Parking Orbit Height [km]"
                    Layout.fillWidth: true
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignTop
                }

                DialogParameter
                {
                    id: _height_periapse_arr_
                    placeholderText: "Arrival Rendezvous Orbit Periapse Height [km]"
                    Layout.fillWidth: true
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignTop
                }

                DialogParameter
                {
                    id: _period_arr_
                    placeholderText: "Arrival Rendezvous Orbit Period [h]"
                    Layout.fillWidth: true
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignTop
                }
            }
        }
    }
}