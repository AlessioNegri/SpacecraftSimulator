import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "../../components/figure"
import "../../components/page"

// * The PageAtmosphericEntry class manages the atmospheric entry page.
Page
{
    // ! ----------------------------------------- ! //
    
    background: Rectangle { color: "#424242" }
    header: PageHeader { p_Title: "Atmospheric Entry" }
    footer: PageFooter {}

    contentItem: Item
    {
        width: parent.width

        Figure
        {
            p_ObjectName: "AtmosphericEntryFigure"
            r_Model: __AtmosphericEntryFigure
            anchors.fill: parent
        }
    }
}