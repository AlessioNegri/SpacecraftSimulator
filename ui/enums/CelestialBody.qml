pragma Singleton

import QtQuick

// * The CelestialBody class manages the celestial body enumaration.
QtObject
{
    // ! ----------------------------------------- ! //

    id: root

    property int sun: 0

    property int mercury: 1

    property int venus: 2

    property int earth: 3

    property int moon: 4

    property int mars: 5

    property int jupiter: 6

    property int saturn: 7

    property int uranus: 8

    property int neptune: 9

    property int pluto: 10
}