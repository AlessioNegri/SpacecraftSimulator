import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "components/page"
import "dialogs"

// * Main window application
ApplicationWindow
{
    // * Previous x position
    property int previousX: 0

    // * Previous y position
    property int previousY: 0

    // * Current page.
    property int gp_CurrentPage: 0

    // * Reference to the Maneuvers array.
    property var gr_Maneuvers: []

    // * Reference to the Maneuver Infos array.
    property var gr_ManeuverInfos: []

    // ! ----------------------------------------- ! //

    id: window
    title: "Spacecraft Simulator"
    visible: true
    visibility: Window.Maximized
    width: 1200
    height: 700
    minimumWidth: 1200
    minimumHeight: 700
    flags: Qt.Window | Qt.FramelessWindowHint
    
    background: Rectangle
    {
        color: "#162A35"
        radius: 5
        border.width: 2
        border.color: "#93F9D8"

        Image
        {
            id: _background_
            source: "/jpg/background.jpg"
            opacity: 0.5
            anchors.fill: parent
            anchors.margins: 2
        }

        Rectangle
        {
            color: "transparent"
            radius: 10
            border.width: 2
            border.color: "#93F9D8"
            anchors.fill: parent
        }

        Rectangle
        {
            color: "transparent"
            radius: 7
            border.width: 2
            border.color: "#93F9D8"
            anchors.fill: parent
        }
    }

    Component.onCompleted:
    {
        console.log("Info")
        console.warn("Warning")
        console.error("Error")
    }

    // * Dialogs

    DialogAbout { id: _dialog_about_ }

    DialogExit { id: _dialog_exit_ }

    DialogSettings { id: _dialog_settings_ }

    onClosing: {

        close.accepted = false

        _dialog_exit_.open()
    }

    // * Side Bar

    SideBar
    {
        id: _side_bar_
        anchors.top: parent.top
        anchors.left: parent.left
        anchors.bottom: parent.bottom
    }

    // * Loader

    Loader
    {
        id: loader
        anchors.fill: parent
        anchors.leftMargin: _side_bar_.width// + 10
        anchors.rightMargin: 3
        anchors.topMargin: 3
        anchors.bottomMargin: 5
        source: "pages/PageHome.qml"
    }

    Item
    {
        id: _expanded_container_
        anchors.fill: parent
        anchors.leftMargin: _side_bar_.width + 10
        anchors.rightMargin: 10
        anchors.topMargin: 60
        anchors.bottomMargin: 10
    }

    Rectangle
    {
        id: notification_box
        width: notification_text.width + 20
        height: notification_text.height + 20
        color: "#8093F9D8"
        radius: 5
        border.width: 2
        border.color: "#93F9D8"
        opacity: 0.0
        anchors.top: parent.top
        anchors.topMargin: 10
        anchors.horizontalCenter: parent.horizontalCenter

        Text
        {
            id: notification_text
            text: ""
            font.pointSize: 10
            font.bold: true
            color: "#FFFFFF"
            anchors.centerIn: parent
        }

        NumberAnimation
        {
            id: notification
            target: notification_box
            properties: "opacity"
            from: 0.0
            to: 1.0
            loops: 1
            duration: 1000
            easing.type: Easing.Linear
            onFinished: notification_close.start()
        }

        NumberAnimation
        {
            id: notification_close
            target: notification_box
            properties: "opacity"
            from: 1.0
            to: 0.0
            loops: 1
            duration: 5000
            easing.type: Easing.InExpo
        }
    }

    // * Resizing

    MouseArea
    {
        height: 5
        anchors.top: parent.top
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.leftMargin: 10
        anchors.rightMargin: 10
        cursorShape: Qt.SizeVerCursor
        onPressed: window.startSystemResize(Qt.TopEdge)
    }

    MouseArea
    {
        width: 5
        anchors.left: parent.left
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        anchors.topMargin: 10
        anchors.bottomMargin: 10
        cursorShape: Qt.SizeHorCursor
        onPressed: window.startSystemResize(Qt.LeftEdge)
    }

    MouseArea
    {
        width: 5
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        anchors.topMargin: 10
        anchors.bottomMargin: 10
        cursorShape: Qt.SizeHorCursor
        onPressed: window.startSystemResize(Qt.RightEdge)
    }

    MouseArea
    {
        height: 5
        anchors.bottom: parent.bottom
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.leftMargin: 10
        anchors.rightMargin: 10
        cursorShape: Qt.SizeVerCursor
        onPressed: window.startSystemResize(Qt.BottomEdge)
    }

    MouseArea
    {
        width: 10
        height: 10
        anchors.top: parent.top
        anchors.left: parent.left
        cursorShape: Qt.SizeFDiagCursor
        onPressed: window.startSystemResize(Qt.TopEdge | Qt.LeftEdge)
    }

    MouseArea
    {
        width: 10
        height: 10
        anchors.top: parent.top
        anchors.right: parent.right
        cursorShape: Qt.SizeBDiagCursor
        onPressed: window.startSystemResize(Qt.TopEdge | Qt.RightEdge)
    }

    MouseArea
    {
        width: 10
        height: 10
        anchors.bottom: parent.bottom
        anchors.left: parent.left
        cursorShape: Qt.SizeBDiagCursor
        onPressed: window.startSystemResize(Qt.BottomEdge | Qt.LeftEdge)
    }

    MouseArea
    {
        width: 10
        height: 10
        anchors.bottom: parent.bottom
        anchors.right: parent.right
        cursorShape: Qt.SizeFDiagCursor
        onPressed: window.startSystemResize(Qt.BottomEdge | Qt.RightEdge)
    }

    /*
    SwipeView
    {
        id: _view_
        currentIndex: 0
        interactive: false
        anchors.fill: parent
        anchors.leftMargin: _drawer_.width + 10
        clip: true

        PageOrbitInsertion
        {
            id: _page_orbit_insertion_
            width: window.width - _drawer_.width - 10
            height: window.height - _menu_bar_.height
        }

        PageOrbitTransfer
        {
            id: _page_orbit_transfer_
            width: window.width - _drawer_.width - 10
            height: window.height - _menu_bar_.height 
        }

        PageOrbitPropagation
        {
            id: _page_orbit_propagation_
            width: window.width - _drawer_.width - 10
            height: window.height - _menu_bar_.height
        }

        PageInterplanetaryTransfer
        {
            id: _page_interplanetary_trensfer_
            width: window.width - _drawer_.width - 10
            height: window.height - _menu_bar_.height
        }

        PageAtmosphericEntry
        {
            id: _page_atmospheric_entry_
            width: window.width - _drawer_.width - 10
            height: window.height - _menu_bar_.height
        }
    }
    */
}