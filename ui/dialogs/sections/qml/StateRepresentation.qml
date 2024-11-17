pragma Singleton

import QtQuick

QtObject
{
    id: singleton

    property int cartesian: 0

    property int keplerian: 1

    property int modifiedKeplerian: 2
}