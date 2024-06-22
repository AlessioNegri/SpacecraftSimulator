import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "../components"

// ? The PageOrbitalPerturbations class manages the orbital perturbations page.
Page
{
    background: Rectangle { color: "transparent" }
    
    Figure {
        p_ObjectName: "OrbitPropagationFigure"
        r_Model: __OrbitPropagationFigure
        anchors.fill: parent
        anchors.margins: 16
    }
}