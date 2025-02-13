pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls.Basic

ComboBox
{
    id: root

    delegate: ItemDelegate
    {
        id: delegate

        required property var model
        required property int index

        width: root.width
        highlighted: root.highlightedIndex === index

        contentItem: Text
        {
            text: delegate.model[root.textRole]
            color: index == root.currentIndex ? "#93F9D8" : "#FFFFFF"
            font: root.font
            elide: Text.ElideRight
            verticalAlignment: Text.AlignVCenter
        }

        background: Rectangle
        {
            color: highlighted ? "#487D76" : "transparent"
            radius: 5
        }
    }

    indicator: Canvas
    {
        id: canvas
        x: root.width - width - root.rightPadding
        y: root.topPadding + (root.availableHeight - height) / 2
        width: 12
        height: 8
        contextType: "2d"

        Connections
        {
            target: root
            function onPressedChanged() { canvas.requestPaint(); }
        }

        onPaint:
        {
            context.reset();
            context.moveTo(0, 0);
            context.lineTo(width, 0);
            context.lineTo(width / 2, height);
            context.closePath();
            context.fillStyle = "#FFFFFF";
            context.fill();
        }
    }

    contentItem: Text
    {
        leftPadding: 10
        rightPadding: root.indicator.width + root.spacing
        text: root.displayText
        font: root.font
        color: root.hovered ? "#93F9D8" : "#FFFFFF"
        verticalAlignment: Text.AlignVCenter
        elide: Text.ElideRight
    }

    background: Rectangle
    {
        implicitWidth: 120
        implicitHeight: 40
        color: "#162A35"
        border.color: root.hovered || root.popup.visible ? "#93F9D8" : "#808080"
        border.width: root.visualFocus ? 2 : 1
        radius: 5
    }

    popup: Popup
    {
        y: root.height - 1
        width: root.width
        height: Math.min(contentItem.implicitHeight, root.Window.height - topMargin - bottomMargin)
        padding: 1

        contentItem: ListView
        {
            clip: true
            implicitHeight: contentHeight
            model: root.popup.visible ? root.delegateModel : null
            currentIndex: root.highlightedIndex
            ScrollIndicator.vertical: ScrollIndicator { }
        }

        background: Rectangle
        {
            color: "#162A35"
            border.color: "#93F9D8"
            radius: 5
        }
    }
}