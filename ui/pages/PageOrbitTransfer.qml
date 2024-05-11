import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "../components"

// ? The PageOrbitTransfer class manages the orbit transfer page.
Page
{
    background: Rectangle { color: "transparent" }

    Figure {
        p_ObjectName: "OrbitTransferFigure"
        r_Model: __OrbitTransferFigure
        anchors.fill: parent
        anchors.margins: 16
    }
}