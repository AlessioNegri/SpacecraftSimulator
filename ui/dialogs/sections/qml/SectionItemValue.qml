import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

TextField
{
    // * True for float numbers.
    property bool p_FloatRegex: true

    // * True for int numbers.
    property bool p_IntRegex: false

    // * Regular expression function.
    function regex()
    {
        if      (p_FloatRegex)  return /[+-]?([0-9]*[.])?[0-9]+/
        else if (p_IntRegex)    return /[0-9]+/
        else                    return /[\s\S]*/
    }

    // ! ----------------------------------------- ! //

    implicitHeight: 40
    Layout.fillWidth: true
    validator: RegularExpressionValidator { regularExpression: regex() }
}