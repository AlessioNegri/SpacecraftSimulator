import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "js/PageOrbitTransferLeft.js" as Script

import "../components/common"
import "../components/material"

import "../enums"

// * The PageOrbitTransferLeft class manages the orbit transfer left page.
ScrollView
{
    // * Selected celestial body.
    property int p_SelectedCelestialBody: CelestialBody.sun

    // * Selected departure state representation.
    property int p_SelectedDepartureSateRepresentation: StateRepresentation.cartesian

    // * Selected arrival state representation.
    property int p_SelectedArrivalSateRepresentation: StateRepresentation.cartesian

    // * Reference to the Maneuvers array.
    property var r_Maneuvers: []

    // * Loads all the parameters.
    function load()
    {
        Script.restoreDepartureParameters()

        Script.restoreArrivalParameters()

        Script.loadManeuvers()
    }

    // * Saves all the parameters.
    function save()
    {
        Script.saveCelestialBody()

        Script.saveDepartureParameters()

        Script.saveArrivalParameters()

        Script.saveManeuvers()

        load()
    }

    // ! ----------------------------------------- ! //

    Component.onCompleted: load()

    width: parent.width
    contentWidth: parent.width
    contentHeight: _layout_.height

    ScrollBar.vertical: MaterialScrollBar { orientation: Qt.Vertical }
    ScrollBar.horizontal: ScrollBar { policy: ScrollBar.AlwaysOff }

    ColumnLayout
    {
        id: _layout_
        width: parent.width - 20
        spacing: 20

        // --- CELESTIAL BODY 

        SectionHeader
        {
            id: _celestial_body_
            p_Title: "Celestial Body"
            p_Icon: "/png/planets.png"
        }

        Flow
        {
            spacing: 20
            visible: !_celestial_body_.p_Hide
            Layout.fillWidth: true

            CelestialBodyIcon
            {
                p_CelestialBody: CelestialBody.sun
                p_Selected: p_SelectedCelestialBody === CelestialBody.sun

                function f_Click() { p_SelectedCelestialBody = CelestialBody.sun }
            }

            CelestialBodyIcon
            {
                p_CelestialBody: CelestialBody.mercury
                p_Selected: p_SelectedCelestialBody === CelestialBody.mercury

                function f_Click() { p_SelectedCelestialBody = CelestialBody.mercury }
            }

            CelestialBodyIcon
            {
                p_CelestialBody: CelestialBody.venus
                p_Selected: p_SelectedCelestialBody === CelestialBody.venus

                function f_Click() { p_SelectedCelestialBody = CelestialBody.venus }
            }

            CelestialBodyIcon
            {
                p_CelestialBody: CelestialBody.earth
                p_Selected: p_SelectedCelestialBody === CelestialBody.earth

                function f_Click() { p_SelectedCelestialBody = CelestialBody.earth }
            }

            CelestialBodyIcon
            {
                p_CelestialBody: CelestialBody.moon
                p_Selected: p_SelectedCelestialBody === CelestialBody.moon

                function f_Click() { p_SelectedCelestialBody = CelestialBody.moon }
            }

            CelestialBodyIcon
            {
                p_CelestialBody: CelestialBody.mars
                p_Selected: p_SelectedCelestialBody === CelestialBody.mars

                function f_Click() { p_SelectedCelestialBody = CelestialBody.mars }
            }

            CelestialBodyIcon
            {
                p_CelestialBody: CelestialBody.jupiter
                p_Selected: p_SelectedCelestialBody === CelestialBody.jupiter

                function f_Click() { p_SelectedCelestialBody = CelestialBody.jupiter }
            }

            CelestialBodyIcon
            {
                p_CelestialBody: CelestialBody.saturn
                p_Selected: p_SelectedCelestialBody === CelestialBody.saturn

                function f_Click() { p_SelectedCelestialBody = CelestialBody.saturn }
            }

            CelestialBodyIcon
            {
                p_CelestialBody: CelestialBody.uranus
                p_Selected: p_SelectedCelestialBody === CelestialBody.uranus

                function f_Click() { p_SelectedCelestialBody = CelestialBody.uranus }
            }

            CelestialBodyIcon
            {
                p_CelestialBody: CelestialBody.neptune
                p_Selected: p_SelectedCelestialBody === CelestialBody.neptune

                function f_Click() { p_SelectedCelestialBody = CelestialBody.neptune }
            }

            CelestialBodyIcon
            {
                p_CelestialBody: CelestialBody.pluto
                p_Selected: p_SelectedCelestialBody === CelestialBody.pluto

                function f_Click() { p_SelectedCelestialBody = CelestialBody.pluto }
            }
        }

        // --- DEPARTURE ORBIT 

        SectionHeader
        {
            id: _departure_orbit_
            p_Title: "Departure Orbit"
            p_Icon: "/png/departure.png"

            RowLayout
            {
                anchors.top: parent.top
                anchors.right: parent.right
                anchors.bottom: parent.bottom
                anchors.rightMargin: 20
                spacing: 10

                MaterialButton
                {
                    text: "Orbit"
                    Layout.alignment: Qt.AlignRight

                    onClicked: {
                        __MissionOrbitTransfer.evaluate_departure_orbit()
                        
                        _departure_orbit_preview_.open()
                    }
                }

                MaterialButton
                {
                    text: "Ground Track"
                    Layout.alignment: Qt.AlignRight
                    
                    onClicked: {
                        __MissionOrbitTransfer.evaluate_departure_ground_track()
                        
                        _departure_ground_track_preview_.open()
                    }
                }
            }
        }

        GridLayout
        {
            rows: 2
            columns: 3
            rowSpacing: 20
            columnSpacing: 20
            uniformCellWidths: true
            visible: !_departure_orbit_.p_Hide
            Layout.fillWidth: true

            RadioButton
            {
                id: _departure_cartesian_
                text: "Cartesian"
                checked: p_SelectedDepartureSateRepresentation === StateRepresentation.cartesian
                Layout.alignment: Qt.AlignHCenter
                onClicked: p_SelectedDepartureSateRepresentation = StateRepresentation.cartesian
            }

            RadioButton
            {
                id: _departure_keplerian_
                text: "Keplerian"
                checked: p_SelectedDepartureSateRepresentation === StateRepresentation.keplerian
                Layout.alignment: Qt.AlignHCenter
                onClicked: p_SelectedDepartureSateRepresentation = StateRepresentation.keplerian
            }

            RadioButton
            {
                id: _departure_modified_keplerian_
                text: "Modified Keplerian"
                checked: p_SelectedDepartureSateRepresentation === StateRepresentation.modifiedKeplerian
                Layout.alignment: Qt.AlignHCenter
                onClicked: p_SelectedDepartureSateRepresentation = StateRepresentation.modifiedKeplerian
            }

            ColumnLayout
            {
                spacing: 20
                Layout.fillWidth: true

                SectionItemValue
                {
                    id: _departure_x_
                    placeholderText: "X [km]"
                    enabled: _departure_cartesian_.checked
                    Layout.fillWidth: true
                }

                SectionItemValue
                {
                    id: _departure_y_
                    placeholderText: "Y [km]"
                    enabled: _departure_cartesian_.checked
                    Layout.fillWidth: true
                }

                SectionItemValue
                {
                    id: _departure_z_
                    placeholderText: "Z [km]"
                    enabled: _departure_cartesian_.checked
                    Layout.fillWidth: true
                }

                SectionItemValue
                {
                    id: _departure_v_x_
                    placeholderText: "Vx [km/s]"
                    enabled: _departure_cartesian_.checked
                    Layout.fillWidth: true
                }

                SectionItemValue
                {
                    id: _departure_v_y_
                    placeholderText: "Vy [km/s]"
                    enabled: _departure_cartesian_.checked
                    Layout.fillWidth: true
                }

                SectionItemValue
                {
                    id: _departure_v_z_
                    placeholderText: "Vz [km/s]"
                    enabled: _departure_cartesian_.checked
                    Layout.fillWidth: true
                }
            }

            ColumnLayout
            {
                spacing: 20
                Layout.fillWidth: true

                SectionItemValue
                {
                    id: _departure_semi_major_axis_
                    placeholderText: "Semi-Major Axis [km]"
                    enabled: _departure_keplerian_.checked
                    Layout.fillWidth: true
                }

                SectionItemValue
                {
                    id: _departure_eccentricity_
                    placeholderText: "Eccentricity"
                    enabled: _departure_keplerian_.checked
                    Layout.fillWidth: true
                }

                SectionItemValue
                {
                    id: _departure_inclination_
                    placeholderText: "Inclination [deg]"
                    enabled: _departure_keplerian_.checked
                    Layout.fillWidth: true
                }

                SectionItemValue
                {
                    id: _departure_raan_
                    placeholderText: "RAAN [deg]"
                    enabled: _departure_keplerian_.checked
                    Layout.fillWidth: true
                }

                SectionItemValue
                {
                    id: _departure_periapsis_anomaly_
                    placeholderText: "Periapsis Anomaly [deg]"
                    enabled: _departure_keplerian_.checked
                    Layout.fillWidth: true
                }

                SectionItemValue
                {
                    id: _departure_true_anomaly_
                    placeholderText: "True Anomaly [deg]"
                    enabled: _departure_keplerian_.checked
                    Layout.fillWidth: true
                }
            }

            ColumnLayout
            {
                spacing: 20
                Layout.fillWidth: true

                SectionItemValue
                {
                    id: _departure_periapsis_radius_
                    placeholderText: "Periapsis Radius [km]"
                    enabled: _departure_modified_keplerian_.checked
                    Layout.fillWidth: true
                }

                SectionItemValue
                {
                    id: _departure_apoapsis_radius_
                    placeholderText: "Apoapsis Radius [km]"
                    enabled: _departure_modified_keplerian_.checked
                    Layout.fillWidth: true
                }

                SectionItemValue
                {
                    id: _departure_inclination_2_
                    placeholderText: "Inclination [deg]"
                    enabled: _departure_modified_keplerian_.checked
                    Layout.fillWidth: true
                }

                SectionItemValue
                {
                    id: _departure_raan_2_
                    placeholderText: "RAAN [deg]"
                    enabled: _departure_modified_keplerian_.checked
                    Layout.fillWidth: true
                }

                SectionItemValue
                {
                    id: _departure_periapsis_anomaly_2_
                    placeholderText: "Periapsis Anomaly [deg]"
                    enabled: _departure_modified_keplerian_.checked
                    Layout.fillWidth: true
                }

                SectionItemValue
                {
                    id: _departure_true_anomaly_2_
                    placeholderText: "True Anomaly [deg]"
                    enabled: _departure_modified_keplerian_.checked
                    Layout.fillWidth: true
                }
            }
        }

        // --- ARRIVAL ORBIT 

        SectionHeader
        {
            id: _arrival_orbit_
            p_Title: "Arrival Orbit"
            p_Icon: "/png/arrival.png"

            RowLayout
            {
                anchors.top: parent.top
                anchors.right: parent.right
                anchors.bottom: parent.bottom
                anchors.rightMargin: 20
                spacing: 10

                MaterialButton
                {
                    text: "Orbit"
                    Layout.alignment: Qt.AlignRight

                    onClicked: {
                        __MissionOrbitTransfer.evaluate_arrival_orbit()
                        
                        _arrival_orbit_preview_.open()
                    }
                }

                MaterialButton
                {
                    text: "Ground Track"
                    Layout.alignment: Qt.AlignRight
                    
                    onClicked: {
                        __MissionOrbitTransfer.evaluate_arrival_ground_track()
                        
                        _arrival_ground_track_preview_.open()
                    }
                }
            }
        }
        
        GridLayout
        {
            rows: 2
            columns: 3
            rowSpacing: 20
            columnSpacing: 20
            uniformCellWidths: true
            visible: !_arrival_orbit_.p_Hide
            Layout.fillWidth: true

            RadioButton
            {
                id: _arrival_cartesian_
                text: "Cartesian"
                checked: p_SelectedArrivalSateRepresentation === StateRepresentation.cartesian
                Layout.alignment: Qt.AlignHCenter
                onClicked: p_SelectedArrivalSateRepresentation = StateRepresentation.cartesian
            }

            RadioButton
            {
                id: _arrival_keplerian_
                text: "Keplerian"
                checked: p_SelectedArrivalSateRepresentation === StateRepresentation.keplerian
                Layout.alignment: Qt.AlignHCenter
                onClicked: p_SelectedArrivalSateRepresentation = StateRepresentation.keplerian
            }

            RadioButton
            {
                id: _arrival_modified_keplerian_
                text: "Modified Keplerian"
                checked: p_SelectedArrivalSateRepresentation === StateRepresentation.modifiedKeplerian
                Layout.alignment: Qt.AlignHCenter
                onClicked: p_SelectedArrivalSateRepresentation = StateRepresentation.modifiedKeplerian
            }

            ColumnLayout
            {
                spacing: 20
                Layout.fillWidth: true

                SectionItemValue
                {
                    id: _arrival_x_
                    placeholderText: "X [km]"
                    enabled: _arrival_cartesian_.checked
                    Layout.fillWidth: true
                }

                SectionItemValue
                {
                    id: _arrival_y_
                    placeholderText: "Y [km]"
                    enabled: _arrival_cartesian_.checked
                    Layout.fillWidth: true
                }

                SectionItemValue
                {
                    id: _arrival_z_
                    placeholderText: "Z [km]"
                    enabled: _arrival_cartesian_.checked
                    Layout.fillWidth: true
                }

                SectionItemValue
                {
                    id: _arrival_v_x_
                    placeholderText: "Vx [km/s]"
                    enabled: _arrival_cartesian_.checked
                    Layout.fillWidth: true
                }

                SectionItemValue
                {
                    id: _arrival_v_y_
                    placeholderText: "Vy [km/s]"
                    enabled: _arrival_cartesian_.checked
                    Layout.fillWidth: true
                }

                SectionItemValue
                {
                    id: _arrival_v_z_
                    placeholderText: "Vz [km/s]"
                    enabled: _arrival_cartesian_.checked
                    Layout.fillWidth: true
                }
            }

            ColumnLayout
            {
                spacing: 20
                Layout.fillWidth: true

                SectionItemValue
                {
                    id: _arrival_semi_major_axis_
                    placeholderText: "Semi-Major Axis [km]"
                    enabled: _arrival_keplerian_.checked
                    Layout.fillWidth: true
                }

                SectionItemValue
                {
                    id: _arrival_eccentricity_
                    placeholderText: "Eccentricity"
                    enabled: _arrival_keplerian_.checked
                    Layout.fillWidth: true
                }

                SectionItemValue
                {
                    id: _arrival_inclination_
                    placeholderText: "Inclination [deg]"
                    enabled: _arrival_keplerian_.checked
                    Layout.fillWidth: true
                }

                SectionItemValue
                {
                    id: _arrival_raan_
                    placeholderText: "RAAN [deg]"
                    enabled: _arrival_keplerian_.checked
                    Layout.fillWidth: true
                }

                SectionItemValue
                {
                    id: _arrival_periapsis_anomaly_
                    placeholderText: "Periapsis Anomaly [deg]"
                    enabled: _arrival_keplerian_.checked
                    Layout.fillWidth: true
                }

                SectionItemValue
                {
                    id: _arrival_true_anomaly_
                    placeholderText: "True Anomaly [deg]"
                    enabled: _arrival_keplerian_.checked
                    Layout.fillWidth: true
                }
            }

            ColumnLayout
            {
                spacing: 20
                Layout.fillWidth: true

                SectionItemValue
                {
                    id: _arrival_periapsis_radius_
                    placeholderText: "Periapsis Radius [km]"
                    enabled: _arrival_modified_keplerian_.checked
                    Layout.fillWidth: true
                }

                SectionItemValue
                {
                    id: _arrival_apoapsis_radius_
                    placeholderText: "Apoapsis Radius [km]"
                    enabled: _arrival_modified_keplerian_.checked
                    Layout.fillWidth: true
                }

                SectionItemValue
                {
                    id: _arrival_inclination_2_
                    placeholderText: "Inclination [deg]"
                    enabled: _arrival_modified_keplerian_.checked
                    Layout.fillWidth: true
                }

                SectionItemValue
                {
                    id: _arrival_raan_2_
                    placeholderText: "RAAN [deg]"
                    enabled: _arrival_modified_keplerian_.checked
                    Layout.fillWidth: true
                }

                SectionItemValue
                {
                    id: _arrival_periapsis_anomaly_2_
                    placeholderText: "Periapsis Anomaly [deg]"
                    enabled: _arrival_modified_keplerian_.checked
                    Layout.fillWidth: true
                }

                SectionItemValue
                {
                    id: _arrival_true_anomaly_2_
                    placeholderText: "True Anomaly [deg]"
                    enabled: _arrival_modified_keplerian_.checked
                    Layout.fillWidth: true
                }
            }
        }

        SectionHeader
        {
            id: _maneuvers_
            p_Title: "Maneuvers"
            p_Icon: "/png/maneuvers.png"

            RowLayout
            {
                anchors.top: parent.top
                anchors.right: parent.right
                anchors.bottom: parent.bottom
                anchors.rightMargin: 20
                spacing: 10

                MaterialIcon
                {
                    source: "/svg/add.svg"
                    baseColor: "#00FF00"
                    tooltip: "Add"

                    function f_Click() { Script.addManeuver() }
                }
            }
        }

        ColumnLayout
        {
            id: _container_
            spacing: 20
            visible: !_maneuvers_.p_Hide
            Layout.fillWidth: true
        }
    }
}