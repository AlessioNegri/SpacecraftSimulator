import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "../../components/figure"
import "../../components/page"

// * The PageOrtbitInsertion class manages the orbit insertion page.
Page
{
    // ! ----------------------------------------- ! //
    
    background: Rectangle { color: "#424242" }
    header: PageHeader { p_Title: "Orbit Insertion" }
    footer: PageFooter {}

    contentItem: Item
    {
        width: parent.width

        Figure
        {
            p_ObjectName: "OrbitInsertionFigure"
            r_Model: __OrbitInsertionFigure
            anchors.fill: parent
        }
    }
}