import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle
{
    // * Celestial body enum.
    property int p_CelestialBody: CelestialBody.sun

    // * Celestial body selected.
    property bool p_Selected: false

    // * Override to implement the "Click" action.
    function f_Click() {}

    // ! ----------------------------------------- ! //

    color: "transparent"
    width: 75
    height: _layout_.height + 20

    Component.onCompleted:
    {
        switch (p_CelestialBody)
        {
            case CelestialBody.sun:     _image_.source = "/png/sun.png";        _name_.text = "Sun";        break
            case CelestialBody.mercury: _image_.source = "/png/mercury.png";    _name_.text = "Mercury";    break
            case CelestialBody.venus:   _image_.source = "/png/venus.png";      _name_.text = "Venus";      break
            case CelestialBody.earth:   _image_.source = "/png/earth.png";      _name_.text = "Earth";      break
            case CelestialBody.moon:    _image_.source = "/png/moon.png";       _name_.text = "Moon";       break
            case CelestialBody.mars:    _image_.source = "/png/mars.png";       _name_.text = "Mars";       break
            case CelestialBody.jupiter: _image_.source = "/png/jupiter.png";    _name_.text = "Jupiter";    break
            case CelestialBody.saturn:  _image_.source = "/png/saturn.png";     _name_.text = "Saturn";     break
            case CelestialBody.uranus:  _image_.source = "/png/uranus.png";     _name_.text = "Uranus";     break
            case CelestialBody.neptune: _image_.source = "/png/neptune.png";    _name_.text = "Neptune";    break
            case CelestialBody.pluto:   _image_.source = "/png/pluto.png";      _name_.text = "Pluto";      break
        }
    }

    Rectangle
    {
        anchors.fill: parent
        radius: 5
        color: Material.color(Material.Amber)
        opacity: 0.25
        visible: p_Selected
    }

    ColumnLayout
    {
        id: _layout_
        spacing: 10
        anchors.centerIn: parent

        Image
        {
            id: _image_
            source: "/png/sun.png"
            sourceSize.width: 40
            sourceSize.height: 40
            Layout.alignment: Qt.AlignHCenter
        }

        Text
        {
            id: _name_
            text: "Sun"
            color: "#FFFFFF"
            font.pointSize: 12
            font.bold: true
            horizontalAlignment: Text.AlignHCenter
            Layout.alignment: Qt.AlignHCenter
        }
    }

    Rectangle
    {
        anchors.fill: parent
        radius: 5
        color: Material.color(Material.Grey)
        opacity: 0.25
        visible: _mouse_area_.containsMouse
    }

    MouseArea
    {
        id: _mouse_area_
        anchors.fill: parent
        cursorShape: Qt.PointingHandCursor
        hoverEnabled: true
        onClicked: f_Click()
    }
}