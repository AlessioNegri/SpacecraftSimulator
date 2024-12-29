import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "../components/page"

// * The PageHome class manages the home page.
Page
{
    // ! ----------------------------------------- ! //

    background: Rectangle { color: "#162A35" }
    header: PageHeader { p_Title: "Home" }
    footer: PageFooter {}

    contentItem: Item
    {
        width: parent.width
    }
}