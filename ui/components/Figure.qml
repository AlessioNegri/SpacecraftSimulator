import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import FigureCanvas 1.0

// ? The Figure class manages the figure object.
Rectangle
{
    // ? Object name for backend accessibility.
    property string p_ObjectName: ""

    // ? Reference to model.
    property var r_Model: null

    //!-----------------------------------------!//

    objectName: p_ObjectName + "Parent"
    anchors.fill: parent
    color: "transparent"
    radius: 5
    border.width: 2
    border.color: Material.color(Material.Indigo)
    
    FigureCanvas {
        objectName: p_ObjectName
        dpi_ratio: Screen.devicePixelRatio
        anchors.fill: parent
        anchors.margins: 10
        
        ToolBar
        {
            padding: 10
            anchors.right: parent.right
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            Material.primary: "#FFFFFF"

            ColumnLayout
            {
                width: parent.width
                height: parent.height

                Item { Layout.fillHeight: true }

                Button
                {
                    font.pointSize: 10
                    font.bold: true
                    icon.source: "/images/img/home.svg"
                    Material.background: Material.Indigo
                    Material.foreground: "#FFFFFF"
                    Layout.alignment: Qt.AlignHCenter
                    onClicked: r_Model.home()
                }

                Button
                {
                    font.pointSize: 10
                    font.bold: true
                    icon.source: "/images/img/arrow_back.svg"
                    Material.background: Material.Indigo
                    Material.foreground: "#FFFFFF"
                    Layout.alignment: Qt.AlignHCenter
                    onClicked: r_Model.back()
                }

                Button
                {
                    font.pointSize: 10
                    font.bold: true
                    icon.source: "/images/img/arrow_forward.svg"
                    Material.background: Material.Indigo
                    Material.foreground: "#FFFFFF"
                    Layout.alignment: Qt.AlignHCenter
                    onClicked: r_Model.forward()
                }

                Button
                {
                    id: _departure_pan_
                    checkable: true
                    font.pointSize: 10
                    font.bold: true
                    icon.source: "/images/img/pan_tool.svg"
                    Material.background: _departure_pan_.checked ? Material.DeepOrange : Material.Indigo
                    Material.foreground: "#FFFFFF"
                    Material.accent: "#FFFFFF"
                    Layout.alignment: Qt.AlignHCenter
                    
                    onClicked:
                    {
                        if (_departure_zoom_.checked) _departure_zoom_.checked = false

                        r_Model.pan()
                    }
                }

                Button
                {
                    id: _departure_zoom_
                    checkable: true
                    font.pointSize: 10
                    font.bold: true
                    icon.source: "/images/img/zoom_in.svg"
                    Material.background: _departure_zoom_.checked ? Material.DeepOrange : Material.Indigo
                    Material.foreground: "#FFFFFF"
                    Material.accent: "#FFFFFF"
                    Layout.alignment: Qt.AlignHCenter

                    onClicked:
                    {
                        if (_departure_pan_.checked) _departure_pan_.checked = false

                        r_Model.zoom()
                    }
                }

                Item { Layout.fillHeight: true }
            }
        }

        TextInput
        {
            text: r_Model.coord
            font.pointSize: 10
            font.bold: true
            readOnly: true
            anchors.right: parent.right
            anchors.bottom: parent.bottom
        }
    }
}