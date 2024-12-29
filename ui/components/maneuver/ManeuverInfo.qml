import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

// * The ManeuverInfo class manages the generic maneuver info.
GridLayout
{
    // * Name of the selected maneuver.
    property int p_Type: 0

    // * Value of the maneuver's delta velocity.
    property string p_DeltaVelocity: "0.0"

    // * Value of the maneuver's delta time.
    property string p_DeltaTime: "0.0"

    // * Value of the maneuver's delta mass.
    property string p_DeltaMass: "0.0"

    // ! ----------------------------------------- ! //

    id: root
    columns: 4
    columnSpacing: 20
    //uniformCellWidths: true
    Layout.fillWidth: true
    Layout.alignment: Qt.AlignHCenter

    Item
    {
        Layout.columnSpan: 4
    }

    Text
    {
        text: {

            switch (p_Type)
            {
                case 0: return "Hohmann Transfer"
                case 1: return "Bi-Elliptic Hohmann Transfer"
                case 2: return "Plane Change Maneuver"
                case 3: return "Apse Line Rotation From Eta"
            }

            return ""
        }

        color: "#FFFFFF"
        font.pointSize: 14
        font.bold: true
        Layout.fillWidth: true
    }

    TextField
    {
        text: p_DeltaVelocity
        implicitHeight: 40
        placeholderText: "Δv [km / s]"
        readOnly: true
    }

    TextField
    {
        text: p_DeltaTime
        implicitHeight: 40
        placeholderText: "Δt [h]"
        readOnly: true
    }

    TextField
    {
        text: p_DeltaMass
        implicitHeight: 40
        placeholderText: "Δm [kg]"
        readOnly: true
    }
}