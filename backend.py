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
    mainChanged = Signal(bool)
    lrChanged = Signal(int)
    batchSChanged = Signal(int)
    bufferSChanged = Signal(int)
    gammaChanged = Signal(int)
    epsSChanged = Signal(int)
    epsEChanged = Signal(int)
    epsDChanged = Signal(int)

    def __init__(self, parent=None):
        QObject.__init__(self, parent)
        self.properties = {
            'mode': False,
            'run': False,
            'run_text': 'Start',
            'main': True
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
            if self.properties['mode']:
                self.setScore('Wait until session end')
                print('Thread started')
                self.condition = Condition()
                self.agent.condition = self.condition
                self.condition.acquire()
                self.agent.STOP_FLAG = not self.properties['run']
                self.thrd = MyThread(self.agent, self.mode)
                self.thrd.start()
                self.condition.notify()
                self.condition.release()
            else:
                self.properties['main'] = not self.properties['main']
                self.mainChanged.emit(self.properties['main'])
                score = self.agent.test()
                self.properties['main'] = not self.properties['main']
                self.mainChanged.emit(self.properties['main'])
                self.properties['run'] = not self.properties['run']
                self.runChanged.emit(self.properties['run'])
                self.setScore(str(round(score, 2)))

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

    # Score
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

    # Main window visible
    @Property(bool, notify=mainChanged)
    def main(self):
        return self.properties['main']

    # Learning rate
    @Property(float, notify=lrChanged)
    def lr(self):
        return self.agent.LR

    @lr.setter
    def setLR(self, text):
        self.agent.LR = text
        self.lrChanged.emit(self.agent.LR)
        return elf.agent.LR

    @lr.getter
    def getLR(self):
        return self.agent.LR

    # Batch size
    @Property(int, notify=batchSChanged)
    def batch_size(self):
        return self.agent.BATCH_SIZE

    @batch_size.setter
    def setBatchS(self, text):
        self.agent.BATCH_SIZE = text
        self.batchSChanged.emit(self.agent.BATCH_SIZE)
        return self.agent.BATCH_SIZE

    @batch_size.getter
    def getBatchS(self):
        return self.agent.BATCH_SIZE

    # Buffer size
    @Property(int, notify=bufferSChanged)
    def buffer_size(self):
        return self.agent.BUFFER_SIZE

    @buffer_size.setter
    def setBufferS(self, text):
        self.agent.BUFFER_SIZE = text
        self.bufferSChanged.emit(self.agent.BUFFER_SIZE)
        return self.agent.BUFFER_SIZE

    @buffer_size.getter
    def getBufferS(self):
        return self.agent.BUFFER_SIZE

    # Gamma
    @Property(float, notify=gammaChanged)
    def gamma(self):
        return self.agent.GAMMA

    @gamma.setter
    def setgamma(self, text):
        self.agent.GAMMA = text
        self.gammaChanged.emit(self.agent.GAMMA)
        return self.agent.GAMMA

    @gamma.getter
    def getgamma(self):
        return self.agent.GAMMA

    # Eps start
    @Property(float, notify=epsSChanged)
    def eps_start(self):
        return self.agent.EPS_START

    @eps_start.setter
    def setepsS(self, text):
        self.agent.EPS_START = text
        self.epsSChanged.emit(self.agent.EPS_START)
        return self.agent.EPS_START

    @eps_start.getter
    def getepsS(self):
        return self.agent.EPS_START

    # Eps end
    @Property(float, notify=epsEChanged)
    def eps_end(self):
        return self.agent.EPS_END

    @eps_end.setter
    def setepsE(self, text):
        self.agent.EPS_END = text
        self.epsEChanged.emit(self.agent.EPS_END)
        return self.agent.EPS_END

    @eps_end.getter
    def getepsE(self):
        return self.agent.EPS_END

# Eps decay
    @Property(float, notify=epsDChanged)
    def eps_decay(self):
        return self.agent.EPS_DECAY

    @eps_decay.setter
    def setepsD(self, text):
        self.agent.EPS_DECAY = text
        self.epsDChanged.emit(self.agent.EPS_DECAY)
        return self.agent.EPS_DECAY

    @eps_decay.getter
    def getepsD(self):
        return self.agent.EPS_DECAY
