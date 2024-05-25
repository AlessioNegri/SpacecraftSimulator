import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

// ? The DialogManeuvers class manages the maneuvers dialog.
Dialog
{
    // ? Reference to the Maneuvers array.
    property var r_Maneuvers: []
    
    // ? Loads the maneuvers from the backend.
    function loadManeuvers()
    {
        // * Clear

        clearManeuvers()

        // * Cycle

        let len = __MissionParameters.maneuversCount()

        for (let i = 0; i < len; ++i)
        {
            // * Retrieve maneuver from backend

            var maneuver = __MissionParameters.getManeuver(i)

            // * Create QML component

            let component = Qt.createComponent("../components/Maneuver.qml")

            if (component.status == Component.Ready)
            {
                var obj = component.createObject(_container_,
                {
                    "p_Id"              : r_Maneuvers.length + 1,
                    "p_Type"            : maneuver.type,
                    "p_Option"          : maneuver.option,
                    "p_OptionValue"     : maneuver.optionValue,
                    "p_DeltaVelocity"   : maneuver.dv,
                    "p_DeltaTime"       : maneuver.dt,
                    "p_DeltaMass"       : maneuver.dm
                })
                
                if (obj == null)
                {
                    console.log("Error creating object")

                    continue
                }

                // * Add and update

                r_Maneuvers.push(obj)

                _scrollView_.contentHeight = (100 + 16) * (r_Maneuvers.length)
            }
            else if (component.status == Component.Error)
            {
                console.log("Error loading component:" + component.errorString())
            }
        }
    }

    // ? Clears the maneuvers.
    function clearManeuvers()
    {
        for (let i = r_Maneuvers.length - 1; i >= 0; --i)
        {
            r_Maneuvers[i].destroy()

            r_Maneuvers.pop()
        }
    }

    // ? Adds a new maneuver.
    function addManeuver()
    {
        // * Create QML component

        let component = Qt.createComponent("../components/Maneuver.qml")

        if (component.status == Component.Ready)
        {
            var obj = component.createObject(_container_, { "p_Id": r_Maneuvers.length + 1 })
            
            if (obj == null)
            {
                console.log("Error creating object")
            }

            // * Add and update

            r_Maneuvers.push(obj)

            _scrollView_.contentHeight = (100 + 16) * (r_Maneuvers.length)
        }
        else if (component.status == Component.Error)
        {
            console.log("Error loading component:" + component.errorString())
        }
    }

    // ? Removes the maneuvers with the given Id.
    function removeManeuver(id)
    {
        for (let i = 0; i < r_Maneuvers.length; ++i)
        {
            if (r_Maneuvers[i].p_Id === id)
            {
                r_Maneuvers[i].destroy()

                r_Maneuvers.splice(i, 1)

                break
            }
        }
    }

    // ? Updates the maneuvers in the backend.
    function saveManeuvers()
    {
        __MissionParameters.clearManeuvers()

        for (let i = 0; i < r_Maneuvers.length; ++i)
        {
            __MissionParameters.addManeuver(r_Maneuvers[i].p_Type, r_Maneuvers[i].p_Option, r_Maneuvers[i].p_OptionValue)
        }

        __MissionParameters.saveManeuvers()

        close()
    }

    //!-----------------------------------------//

    anchors.centerIn: parent
    modal: true
    closePolicy: Popup.NoAutoClose
    font.pointSize: 14
    width: 1400
    height: 700

    onVisibleChanged: if (visible) loadManeuvers()

    header: Item
    {
        width: parent.width
        height: 75

        Text
        {
            text: "Maneuvers"
            padding: 20
            font.pointSize: 24
            font.bold: true
            color: Material.color(Material.Indigo)
        }
    }

    footer: Item
    {
        width: parent.width
        height: 70
        
        RowLayout
        {
            width: parent.width

            Item { width: 10 }

            Button
            {
                icon.source: "/images/img/add.svg"
                font.pointSize: 12
                font.bold: true
                Material.background: Material.Orange
                Material.foreground: "#FFFFFF"
                onClicked: addManeuver()
            }

            Item { Layout.fillWidth: true }

            Button
            {
                text: "Save"
                font.pointSize: 12
                font.bold: true
                Layout.alignment: Qt.AlignRight
                Material.background: Material.Indigo
                Material.foreground: "#FFFFFF"
                onClicked: saveManeuvers()
            }

            Button
            {
                text: "Close"
                font.pointSize: 12
                font.bold: true
                Layout.alignment: Qt.AlignRight
                Material.background: Material.Grey
                Material.foreground: "#FFFFFF"
                onClicked: close()
            }

            Item { width: 10 }
        }
    }

    Flickable
    {
        id: _scrollView_
        clip: true
        boundsBehavior: Flickable.StopAtBounds
        anchors.fill: parent
        anchors.leftMargin: 16
        anchors.rightMargin: 16
        anchors.topMargin: 16
        anchors.bottomMargin: 16
        width: parent.width - 32
        height: parent.height - 32
        contentWidth: parent.width - 32
        //contentHeight: Screen.desktopAvailableHeight - 32

        ScrollBar.vertical: ScrollBar { parent: _scrollView_; orientation: Qt.Vertical }

        ScrollBar.horizontal: ScrollBar { parent: _scrollView_; orientation: Qt.Horizontal }

        ColumnLayout
        {
            id: _container_
            spacing: 16
            width: parent.width
            //height: _root_.height - 32
        }
    }
}