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

    // ? True for int numbers.
    property bool p_IntRegex: false

    // ! ----------------------------------------- ! //
    
    implicitWidth: 200
    implicitHeight: 40
    placeholderText: p_Name + " " + p_Unit
    font.pointSize: 12

    validator: RegularExpressionValidator
    {
        regularExpression:
        {
            if (p_IntRegex) return /[0-9]+/

            if (p_FloatRegex) return /[+-]?([0-9]*[.])?[0-9]+/

            return p_Regex
        }
    }
}