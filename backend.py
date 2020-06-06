import sys
from PySide2.QtCore import QObject, Signal, Property, QUrl
from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine
from PIL import Image
from agent import Agent
from threading import Thread, Condition


class MyThread(Thread):
    """
    A threading example
    """

    def __init__(self, agent, mode):
        super().__init__()
        """Инициализация потока"""
        self.agent = agent
        self.mode = mode

    def run(self):
        """Запуск потока"""
        if self.mode:
            self.agent.learn_model()
        else:
            self.agent.test()
        print('Agent thread')


class Backend(QObject):
    modeChanged = Signal(bool)
    runChanged = Signal(bool)
    scoreChanged = Signal(str)

    def __init__(self, parent=None):
        QObject.__init__(self, parent)
        self.properties = {
            'mode': False,
            'run': False,
            'run_text': 'Start',
        }
        self.agent = Agent('cpu')

    # Learning mode
    @Property(bool, notify=modeChanged)
    def mode(self):
        return self.properties['mode']

    @mode.setter
    def setMode(self, text):
        if self.properties['run'] == True:
            return
        self.properties['mode'] = text
        self.modeChanged.emit(self.properties['mode'])

    @mode.getter
    def getMode(self):
        return self.properties['mode']

    # Start/stop button
    @Property(bool, notify=runChanged)
    def run(self):
        return self.properties['run']

    @run.setter
    def setRun(self, text):
        if self.properties['run'] == text:
            return
        self.properties['run'] = text
        if self.properties['run']:
            print('Thread started')
            self.condition = Condition()
            self.agent.condition = self.condition
            self.condition.acquire()
            self.agent.STOP_FLAG = not self.properties['run']
            self.thrd = MyThread(self.agent, self.mode)
            self.thrd.start()
            self.condition.notify()
            self.condition.release()
            self.setScore('Wait until session end')
        else:
            self.condition.acquire()
            self.agent.STOP_FLAG = not self.properties['run']
            self.condition.notify()
            self.condition.release()
            self.thrd.join()
            self.setScore(str(round(self.agent.score, 2)))
            print('Thread joined')
        self.runChanged.emit(self.properties['run'])

    @run.getter
    def getRun(self):
        return self.properties['run']

    @Property(str, notify=scoreChanged)
    def score(self):
        return self.agent.score

    @score.setter
    def setScore(self, text):
        self.agent.score = text
        self.scoreChanged.emit(self.agent.score)
        return self.agent.score

    @score.getter
    def getScore(self):
        return self.agent.score
