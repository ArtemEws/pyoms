import QtQuick 2.10
import QtQuick.Controls 2.15
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


    Switch {
        function click(){
            if(backend.run){
                toggle()
            }
            else{
                backend.mode = !backend.mode
            }
        }
        id: switchMode
        x: 0
        y: 580
        width: 278
        height: 140
        text: qsTr("Learning mode")
        onClicked:  click()
    }

    Frame {
        id: frame_for_score
        x: 971
        y: 588
        width: 309
        height: 132
        visible: true
        antialiasing: true
        Text {
            function newscore(){
                return(backend.score)
            }
            text: newscore()
            font.family: "Helvetica"
            font.pointSize: 24
        }
    }

    Frame {
        id: frame_for_agent
        x: 0
        y: 0
        width: 1280
        height: 574

        GridView {
            visible: true
            width: 300; height: 200

            model: none
            delegate: Column {
                Image { source: portrait; anchors.horizontalCenter: parent.horizontalCenter }
                Text { text: name; anchors.horizontalCenter: parent.horizontalCenter }
            }
        }
    }

    Button {
        function changeText() {
            if (backend.run == true) {
                return('Stop')
            }
            else{
                return('Start')
            }
        }
        id: button_start
        x: 575
        y: 623
        width: 130
        height: 62
        text: changeText()
        font.bold: true
        font.italic: false
        font.pointSize: 17
        onClicked: backend.run = !backend.run
    }

    Grid {
        id: grid
        x: 0
        y: 0
        width: 1280
        height: 727
    }
}
}