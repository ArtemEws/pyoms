import QtQuick 2.10
import QtQuick.Controls 2.15
import QtQuick.Window 2.2
import QtQuick.Layouts 1.11


ApplicationWindow {
    title: qsTr("LunarLander V2.0 by Pyoms")
    width: 300
    height: 600
    visible: backend.main

GridLayout {
       id: grid
       anchors.fill: parent
       rows: 10
       columns: 1
    
    TextEdit {
        id: lr
        width: 260
        text: backend.lr
        anchors.leftMargin: 10
        font.family: "Helvetica"
        font.pointSize: 20
        Layout.row: 1
        property string placeholderText: "Learning rate"
        Layout.alignment: Qt.AlignCenter
            Text {

                text: lr.placeholderText
                color: "#aaa"
                visible: !lr.text && !lr.activeFocus
            }
    }

    TextEdit {
        id: batch_size
        width: 260
        text: backend.batch_size
        anchors.leftMargin: 10
        font.family: "Helvetica"
        font.pointSize: 20
        Layout.row: 2
        property string placeholderText: "Batch size"
        Layout.alignment: Qt.AlignCenter
            Text {

                text: batch_size.placeholderText
                color: "#aaa"
                visible: !batch_size.text && !batch_size.activeFocus
            }
    }

    TextEdit {
        id: buffer_size
        width: 260
        text: backend.buffer_size
        anchors.leftMargin: 10
        font.family: "Helvetica"
        font.pointSize: 20
        Layout.row: 3
        property string placeholderText: "Buffer size"
        Layout.alignment: Qt.AlignCenter
            Text {

                text: buffer_size.placeholderText
                color: "#aaa"
                visible: !buffer_size.text && !buffer_size.activeFocus
            }
    }

    TextEdit {
        id: gamma
        width: 260
        text: backend.gamma
        anchors.leftMargin: 10
        font.family: "Helvetica"
        font.pointSize: 20
        Layout.row: 4
        property string placeholderText: "Gamma"
        Layout.alignment: Qt.AlignCenter
            Text {

                text: gamma.placeholderText
                color: "#aaa"
                visible: !gamma.text && !gamma.activeFocus
            }
    }

    TextEdit {
        id: eps_start
        width: 260
        text: backend.eps_start
        anchors.leftMargin: 10
        font.family: "Helvetica"
        font.pointSize: 20
        Layout.row: 5
        property string placeholderText: "Eps start"
        Layout.alignment: Qt.AlignCenter
            Text {

                text: eps_start.placeholderText
                color: "#aaa"
                visible: !eps_start.text && !eps_start.activeFocus
            }
    }

    TextEdit {
        id: eps_end
        width: 260
        text: backend.eps_end
        anchors.leftMargin: 10
        font.family: "Helvetica"
        font.pointSize: 20
        Layout.row: 6
        property string placeholderText: "Eps end"
        Layout.alignment: Qt.AlignCenter
            Text {

                text: eps_end.placeholderText
                color: "#aaa"
                visible: !eps_end.text && !eps_end.activeFocus
            }
    }

        TextEdit {
        id: eps_decay
        width: 260
        text: backend.eps_decay
        anchors.leftMargin: 10
        font.family: "Helvetica"
        font.pointSize: 20
        Layout.row: 7
        property string placeholderText: "Eps decay"
        Layout.alignment: Qt.AlignCenter
            Text {

                text: eps_decay.placeholderText
                color: "#aaa"
                visible: !eps_decay.text && !eps_decay.activeFocus
            }
    }

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
        width: 300
        height: 100
        text: qsTr("Learning mode")
        onClicked:  click()
        Layout.row: 8
        Layout.alignment: Qt.AlignCenter
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
        width: 100
        height: 62
        text: changeText()
        font.bold: true
        font.italic: false
        font.pointSize: 17
        onClicked: backend.run = !backend.run
        Layout.row: 9
        Layout.alignment: Qt.AlignCenter
    }
        Text {
            function newscore(){
                return(backend.score)
            }
            text: newscore()
            font.family: "Helvetica"
            font.pointSize: 24
            Layout.row: 10
            Layout.alignment: Qt.AlignCenter
        }
}
}