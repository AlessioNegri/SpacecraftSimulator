import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
        
TextField
{
    // ? Parameter name.
    property string p_Name: ""

    // ? Parameter unit of measure.
    property string p_Unit: ""

    // ? Value regular expression.
    property var p_Regex: /[\s\S]*/

    // ? True for float numbers.
    property bool p_FloatRegex: true

    // !-----------------------------------------! //
    
    implicitWidth: 200
    implicitHeight: 40
    placeholderText: p_Name + " " + p_Unit
    font.pointSize: 12

    validator: RegularExpressionValidator
    {
        regularExpression: p_FloatRegex ? /[+-]?([0-9]*[.])?[0-9]+/ : p_Regex
    }
}