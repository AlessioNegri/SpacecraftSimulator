import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "../components"

// ? The PageInterplanetaryTransfer class manages the interplanetary transfer page.
Page
{
    background: Rectangle { color: "transparent" }

    Figure {
        p_ObjectName: "InterplanetaryTransferFigure"
        r_Model: __InterplanetaryTransferFigure
        anchors.fill: parent
        anchors.margins: 16
    }
}