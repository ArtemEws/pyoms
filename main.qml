import QtQuick 2.10
import QtQuick.Controls 2.1
import QtQuick.Window 2.2
import QtQuick.Layouts 1.11


ApplicationWindow {
    title: qsTr("LunarLander V2.0 by Pyoms")
    width: 1280
    height: 720
    visible: true

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
    
    Text {
        id: element
        x: 702
        y: 8
        text: qsTr("    BATCH_SIZE = 64\n    BUFFER_SIZE = 100000\n    GAMMA = .99\n    EPS_START = .9\n    EPS_END = .05\n    EPS_DECAY = .995\n    LR = .0016")
        font.pixelSize: 41
    }

    Text {
        id: element1
        x: 807
        y: 625
        text: qsTr("Current score:")
        renderType: Text.NativeRendering
        font.pixelSize: 43
    }
}
}
