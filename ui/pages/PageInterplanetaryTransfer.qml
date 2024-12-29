import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "../components/material"
import "../components/figure"
import "../components/page"

// * The PageInterplanetaryTransfer class manages the interplanetary transfer page.
Page
{
    // ! ----------------------------------------- ! //

    Component.onCompleted: __MissionInterplanetaryTransfer.attach_canvas()
    Component.onDestruction: __MissionInterplanetaryTransfer.detach_canvas()

    background: Rectangle { color: "#162A35" }
    header: PageHeader { p_Title: "Interplanetary Transfer"; p_Source: "/png/interplanetary_transfer.png" }

    contentItem: Item
    {
        GridLayout
        {
            rows: 2
            columns: 2
            rowSpacing: 10
            columnSpacing: 10
            uniformCellHeights: true
            uniformCellWidths: true
            anchors.fill: parent
            anchors.margins: 10

            PageBox
            {
                Layout.rowSpan: 2
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
                            text: "Parameters"
                            font.pointSize: 20
                            font.bold: true
                            color: "#93F9D8"
                        }

                        Item
                        {
                            Layout.fillWidth: true
                        }

                        MaterialIcon
                        {
                            source: "/svg/save.svg"
                            tooltip: "Save"
                            tooltipLocation: Qt.AlignTop

                            function f_Click()
                            {
                                _section_.save()

                                notification_text.text = "Parameters Saved"
                                
                                notification.start()
                            }
                        }

                        MaterialIcon
                        {
                            source: "/svg/play_arrow.svg"
                            baseColor: "#00FF00"
                            tooltip: "Simulate"
                            tooltipLocation: Qt.AlignTop

                            function f_Click() { __MissionInterplanetaryTransfer.simulate() }
                        }
                    }

                    Rectangle
                    {
                        height: 3
                        color: Material.color(Material.Grey)
                        Layout.fillWidth: true
                        Layout.alignment: Qt.AlignBottom
                    }

                    PageInterplanetaryTransferLeft
                    {
                        id: _section_
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                    }
                }
            }

            Item
            {
                id: _figure_container_
                Layout.fillWidth: true
                Layout.fillHeight: true

                Figure
                {
                    p_ObjectName: "InterplanetaryTransferFigure"
                    r_Model: __InterplanetaryTransferFigure
                    r_OriginalParent: _figure_container_
                    r_ExpandedParent: _expanded_container_
                    anchors.fill: parent
                }
            }

            Item
            {
                id: _pork_chop_plot_figure_container_
                Layout.fillWidth: true
                Layout.fillHeight: true

                Figure
                {
                    p_ObjectName: "PorkChopPlotFigure"
                    r_Model: __PorkChopPlotFigure
                    r_OriginalParent: _pork_chop_plot_figure_container_
                    r_ExpandedParent: _expanded_container_
                    anchors.fill: parent
                }
            }
        }
    }
}