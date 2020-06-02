import QtQuick 2.12
import untitled 1.0
import QtQuick.Studio.Components 1.0
import QtQuick.Studio.Effects 1.0
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.11
import Qt.SafeRenderer 1.1
import QtQuick3D 1.15

Rectangle {
    id: rectangle
    width: 1280
    height: 720
    visible: true


    SwitchDelegate {
        id: switch_Play_or_Education
        x: 0
        y: 580
        width: 278
        height: 140
        text: qsTr("Play/Education ")
    }

    Frame {
        id: frame_for_score
        x: 971
        y: 588
        width: 309
        height: 132
        visible: true
        antialiasing: true
    }

    Frame {
        id: frame_for_agent
        x: 0
        y: 0
        width: 1280
        height: 574

        RowLayout {
            id: rowLayout_for_settings
            x: 276
            y: 225
            width: 533
            height: 221
            spacing: 6.2
        }
    }

    Button {
        id: button_start
        x: 575
        y: 623
        width: 130
        height: 62
        text: "Start "
        font.bold: true
        font.italic: false
        font.pointSize: 17
    }

    Grid {
        id: grid
        x: 0
        y: 0
        width: 1280
        height: 727
    }
}

/*##^##
Designer {
    D{i:0;3d-active-scene:-1;autoSize:true;height:480;width:640}
}
##^##*/
