pragma Singleton

import QtQuick

// * The StateRepresentation class manages the state representation enumaration.
QtObject
{
    // ! ----------------------------------------- ! //

    id: root

    property int cartesian: 0

    property int keplerian: 1

    property int modifiedKeplerian: 2
}