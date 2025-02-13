import QtQuick

Rectangle
{
    width: 300
    height: 300
    color: 

    Image
    {
        sourceSize.width: parent.width
        sourceSize.height: parent.height
        fillMode: Image.PreserveAspectFit
    }
}