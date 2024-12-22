import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "../../components/figure"
import "../../components/page"

// * The PageOrbitPropagation class manages the orbit propagation page.
Page
{
    // ! ----------------------------------------- ! //

    background: Rectangle { color: "#424242" }
    header: PageHeader { p_Title: "Orbit Propagation" }
    footer: PageFooter {}

    contentItem: Item
    {
        width: parent.width

        Figure
        {
            p_ObjectName: "OrbitPropagationFigure"
            r_Model: __OrbitPropagationFigure
            anchors.fill: parent
        }
    }
}