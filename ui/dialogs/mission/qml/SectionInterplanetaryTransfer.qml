import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "../js/SectionInterplanetaryTransfer.js" as Script

import "../../common"
import "../../../components/material"

// * The SectionInterplanetaryTransfer class manages the interplanetary transfer section.
ScrollView
{
    // * Selected departure planet.
    property int p_SelectedDeparturePlanet: Planet.earth

    // * Selected arrival planet.
    property int p_SelectedArrivalPlanet: Planet.mars

    // * Loads all the parameters.
    function load()
    {
       Script.restoreParameters()
    }

    // * Saves all the parameters.
    function save()
    {
        Script.saveParameters()

        load()
    }

    // ! ----------------------------------------- ! //

    width: parent.width
    contentWidth: parent.width
    contentHeight: _layout_.height
    onVisibleChanged: if (visible) load()
    
    Component.onCompleted: __MissionInterplanetaryTransfer.signal_update_progress_bar.connect(Script.updateProgressBar)

    ScrollBar.vertical: MaterialScrollBar { orientation: Qt.Vertical }

    ColumnLayout
    {
        id: _layout_
        width: parent.width - 20
        spacing: 20

        // --- DEPARTURE PLANET 

        SectionHeader
        {
            id: _departure_planet_
            p_Title: "Departure Planet"
            p_Icon: "/png/departure.png"
        }

        Flow
        {
            spacing: 20
            visible: !_departure_planet_.p_Hide
            Layout.fillWidth: true

            CelestialBodyIcon
            {
                p_CelestialBody: CelestialBody.mercury
                p_Selected: p_SelectedDeparturePlanet === Planet.mercury

                function f_Click() { p_SelectedDeparturePlanet = Planet.mercury }
            }

            CelestialBodyIcon
            {
                p_CelestialBody: CelestialBody.venus
                p_Selected: p_SelectedDeparturePlanet === Planet.venus

                function f_Click() { p_SelectedDeparturePlanet = Planet.venus }
            }

            CelestialBodyIcon
            {
                p_CelestialBody: CelestialBody.earth
                p_Selected: p_SelectedDeparturePlanet === Planet.earth

                function f_Click() { p_SelectedDeparturePlanet = Planet.earth }
            }

            CelestialBodyIcon
            {
                p_CelestialBody: CelestialBody.mars
                p_Selected: p_SelectedDeparturePlanet === Planet.mars

                function f_Click() { p_SelectedDeparturePlanet = Planet.mars }
            }

            CelestialBodyIcon
            {
                p_CelestialBody: CelestialBody.jupiter
                p_Selected: p_SelectedDeparturePlanet === Planet.jupiter

                function f_Click() { p_SelectedDeparturePlanet = Planet.jupiter }
            }

            CelestialBodyIcon
            {
                p_CelestialBody: CelestialBody.saturn
                p_Selected: p_SelectedDeparturePlanet === Planet.saturn

                function f_Click() { p_SelectedDeparturePlanet = Planet.saturn }
            }

            CelestialBodyIcon
            {
                p_CelestialBody: CelestialBody.uranus
                p_Selected: p_SelectedDeparturePlanet === Planet.uranus

                function f_Click() { p_SelectedDeparturePlanet = Planet.uranus }
            }

            CelestialBodyIcon
            {
                p_CelestialBody: CelestialBody.neptune
                p_Selected: p_SelectedDeparturePlanet === Planet.neptune

                function f_Click() { p_SelectedDeparturePlanet = Planet.neptune }
            }

            CelestialBodyIcon
            {
                p_CelestialBody: CelestialBody.pluto
                p_Selected: p_SelectedDeparturePlanet === Planet.pluto

                function f_Click() { p_SelectedDeparturePlanet = Planet.pluto }
            }
        }

        GridLayout
        {
            rows: 2
            columns: 3
            rowSpacing: 20
            columnSpacing: 20
            uniformCellWidths: true
            visible: !_departure_planet_.p_Hide
            Layout.fillWidth: true

            SectionItemValue
            {
                id: _departure_date_
                placeholderText: "Departure Date"
                inputMask: "0000-00-00 00:00:00;0"
                p_FloatRegex: false
            }

            SectionItemValue
            {
                id: _departure_height_
                placeholderText: "Departure Parking Orbit Height [km]"
            }
        }

        // --- ARRIVAL PLANET 

        SectionHeader
        {
            id: _arrival_planet_
            p_Title: "Arrival Planet"
            p_Icon: "/png/arrival.png"
        }

        Flow
        {
            spacing: 20
            visible: !_arrival_planet_.p_Hide
            Layout.fillWidth: true

            CelestialBodyIcon
            {
                p_CelestialBody: CelestialBody.mercury
                p_Selected: p_SelectedArrivalPlanet === Planet.mercury

                function f_Click() { p_SelectedArrivalPlanet = Planet.mercury }
            }

            CelestialBodyIcon
            {
                p_CelestialBody: CelestialBody.venus
                p_Selected: p_SelectedArrivalPlanet === Planet.venus

                function f_Click() { p_SelectedArrivalPlanet = Planet.venus }
            }

            CelestialBodyIcon
            {
                p_CelestialBody: CelestialBody.earth
                p_Selected: p_SelectedArrivalPlanet === Planet.earth

                function f_Click() { p_SelectedArrivalPlanet = Planet.earth }
            }

            CelestialBodyIcon
            {
                p_CelestialBody: CelestialBody.mars
                p_Selected: p_SelectedArrivalPlanet === Planet.mars

                function f_Click() { p_SelectedArrivalPlanet = Planet.mars }
            }

            CelestialBodyIcon
            {
                p_CelestialBody: CelestialBody.jupiter
                p_Selected: p_SelectedArrivalPlanet === Planet.jupiter

                function f_Click() { p_SelectedArrivalPlanet = Planet.jupiter }
            }

            CelestialBodyIcon
            {
                p_CelestialBody: CelestialBody.saturn
                p_Selected: p_SelectedArrivalPlanet === Planet.saturn

                function f_Click() { p_SelectedArrivalPlanet = Planet.saturn }
            }

            CelestialBodyIcon
            {
                p_CelestialBody: CelestialBody.uranus
                p_Selected: p_SelectedArrivalPlanet === Planet.uranus

                function f_Click() { p_SelectedArrivalPlanet = Planet.uranus }
            }

            CelestialBodyIcon
            {
                p_CelestialBody: CelestialBody.neptune
                p_Selected: p_SelectedArrivalPlanet === Planet.neptune

                function f_Click() { p_SelectedArrivalPlanet = Planet.neptune }
            }

            CelestialBodyIcon
            {
                p_CelestialBody: CelestialBody.pluto
                p_Selected: p_SelectedArrivalPlanet === Planet.pluto

                function f_Click() { p_SelectedArrivalPlanet = Planet.pluto }
            }
        }

        GridLayout
        {
            rows: 2
            columns: 3
            rowSpacing: 20
            columnSpacing: 20
            uniformCellWidths: true
            visible: !_arrival_planet_.p_Hide
            Layout.fillWidth: true

            SectionItemValue
            {
                id: _arrival_date_
                placeholderText: "Arrival Date"
                inputMask: "0000-00-00 00:00:00;0"
                p_FloatRegex: false
            }

            SectionItemValue
            {
                id: _arrival_height_
                placeholderText: "Arrival Rendezvous Orbit Periapse Height [km]"
            }

            SectionItemValue
            {
                id: _arrival_period_
                placeholderText: "Arrival Rendezvous Orbit Period [h]"
            }
        }

        // --- PORK CHOP PLOT 

        SectionHeader
        {
            id: _pork_chop_plot_
            p_Title: "Pork Chop Plot"
            p_Icon: "/png/plot.png"

            RowLayout
            {
                anchors.top: parent.top
                anchors.right: parent.right
                anchors.bottom: parent.bottom
                anchors.rightMargin: 20
                spacing: 10

                Button
                {
                    text: "Show"
                    font.pointSize: 12
                    font.bold: true
                    Layout.alignment: Qt.AlignRight
                    Material.background: "#009688"
                    Material.foreground: "#FFFFFF"
                    onClicked: _porkChopPlot_.open()
                }

                Button
                {
                    text: "Generate"
                    font.pointSize: 12
                    font.bold: true
                    Layout.alignment: Qt.AlignRight
                    Material.background: "#009688"
                    Material.foreground: "#FFFFFF"
                    onClicked: __MissionInterplanetaryTransfer.generate_pork_chop_plot()
                }

                Button
                {
                    text: "Stop"
                    font.pointSize: 12
                    font.bold: true
                    Layout.alignment: Qt.AlignRight
                    Material.background: "#009688"
                    Material.foreground: "#FFFFFF"
                    onClicked: __MissionInterplanetaryTransfer.stop_generate_pork_chop_plot()
                }
            }
        }

        GridLayout
        {
            rows: 2
            columns: 4
            rowSpacing: 20
            columnSpacing: 20
            uniformCellWidths: true
            visible: !_pork_chop_plot_.p_Hide
            Layout.fillWidth: true

            SectionItemValue
            {
                id: _launch_window_begin_
                placeholderText: "Launch Window Begin"
                inputMask: "0000-00-00;0"
                p_FloatRegex: false
            }

            SectionItemValue
            {
                id: _launch_window_end_
                placeholderText: "Launch Window End"
                inputMask: "0000-00-00;0"
                p_FloatRegex: false
            }

            SectionItemValue
            {
                id: _arrival_window_begin_
                placeholderText: "Arrival Window Begin"
                inputMask: "0000-00-00;0"
                p_FloatRegex: false
            }

            SectionItemValue
            {
                id: _arrival_window_end_
                placeholderText: "Arrival Window End"
                inputMask: "0000-00-00;0"
                p_FloatRegex: false
            }

            SectionItemValue
            {
                id: _window_step_
                placeholderText: "Window Step"
                p_IntRegex: true
            }

            MaterialProgressBar
            {
                id: _progressBar_
                implicitHeight: 40
                Layout.columnSpan: 3
                Layout.fillWidth: true
            }
        }
    }
}