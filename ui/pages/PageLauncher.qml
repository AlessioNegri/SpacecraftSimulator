import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "../components/material"
import "../components/page"

// * The PageHome class manages the home page.
Page
{
    // * Selected stage.
    property int p_CurrentStage: 1

    // ! ----------------------------------------- ! //

    Component.onCompleted: {

        _stage_1_.p_InUse = __MissionOrbitInsertion.use_stage_1
        _stage_2_.p_InUse = __MissionOrbitInsertion.use_stage_2
        _stage_3_.p_InUse = __MissionOrbitInsertion.use_stage_3
    }

    //background: Rectangle { color: "#162A35" }
    header: PageHeader { p_Title: "Launcher"; p_Source: "/png/launcher.png" }
    footer: PageFooter {}

    contentItem: Item
    {
        RowLayout
        {
            spacing: 10
            anchors.fill: parent
            anchors.margins: 10

            PageBox
            {
                Layout.fillWidth: true
                Layout.fillHeight: true

                ColumnLayout
                {
                    anchors.fill: parent
                    anchors.margins: 10

                    RowLayout
                    {
                        Layout.fillWidth: true
                        spacing: 10

                        Text
                        {
                            font.pointSize: 20
                            font.bold: true
                            color: "#93F9D8"

                            text:
                            {
                                switch (p_CurrentStage)
                                {
                                    case 0: return "Payload"
                                    case 1: return "Stage 1"
                                    case 2: return "Stage 2"
                                    case 3: return "Stage 3"
                                }
                            }
                        }

                        Item
                        {
                            Layout.fillWidth: true
                        }

                        MaterialIcon
                        {
                            source: "/svg/save.svg"

                            function f_Click()
                            {
                                _section_.save()

                                notification_text.text = "Parameters Saved"
                                
                                notification.start()
                            }
                        }
                    }

                    Rectangle
                    {
                        height: 3
                        radius: 10
                        color: Material.color(Material.Grey)
                        Layout.fillWidth: true
                        Layout.alignment: Qt.AlignBottom
                    }

                    PageLauncherLeft
                    {
                        id: _section_
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                    }
                }
            }

            PageBox
            {
                width: 300
                Layout.fillHeight: true

                ColumnLayout
                {
                    spacing: 10
                    width: parent.width
                    height: parent.height

                    Stage
                    {
                        id: _payload_
                        p_Source: "/png/launcher_payload.png"
                        p_Text: "PAYLOAD"
                        p_Selected: p_CurrentStage === 0
                        p_InUse: true

                        function f_Click() { _section_.p_CurrentStage = p_CurrentStage = 0 }
                    }

                    Stage
                    {
                        id: _stage_3_
                        p_Source: "/png/launcher_stage_3.png"
                        p_Text: "STAGE 3"
                        p_Selected: p_CurrentStage === 3

                        function f_Click() { _section_.p_CurrentStage = p_CurrentStage = 3 }
                    }

                    Stage
                    {
                        id: _stage_2_
                        p_Source: "/png/launcher_stage_2.png"
                        p_Text: "STAGE 2"
                        p_Selected: p_CurrentStage === 2

                        function f_Click() { _section_.p_CurrentStage = p_CurrentStage = 2 }
                    }

                    Stage
                    {
                        id: _stage_1_
                        p_Source: "/png/launcher_stage_1.png"
                        p_Text: "STAGE 1"
                        p_Selected: p_CurrentStage === 1

                        function f_Click() { _section_.p_CurrentStage = p_CurrentStage = 1 }
                    }
                }
            }
        }
    }
}