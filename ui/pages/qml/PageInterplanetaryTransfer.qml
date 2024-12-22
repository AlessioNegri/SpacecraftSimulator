import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "../../components/figure"
import "../../components/page"

// * The PageInterplanetaryTransfer class manages the interplanetary transfer page.
Page
{
    // ! ----------------------------------------- ! //

    background: Rectangle { color: "#424242" }
    header: PageHeader { p_Title: "Interplanetary Transfer" }
    footer: PageFooter {}

    contentItem: Item
    {
        width: parent.width
    
        Figure
        {
            p_ObjectName: "InterplanetaryTransferFigure"
            r_Model: __InterplanetaryTransferFigure
            anchors.fill: parent
        }
    }
}