#Written by Alex I. Ramirez @alexram1313
#arcompware.com
#Python 3!!!!!!

import subprocess
import _thread

class PiFmQueue:

    '''
    Initializes the class to command to broadcast at a specified frequency
    '''
    def __init__(self, frequency):
        self._freq = frequency
        self._queue = []

    '''
    Prints self._queue
    '''
    def print_queue(self):
        print(self._queue)

    '''
    Starts the subprocess to pipe audio into pifm
    '''
    def _play_sound(self, filename ):
        #Change './pi2fm' to the name of the compiled program for PiFM
        #i.e. './pifm' or './pi2fm'
        subprocess.call(
            'avconv -i "{0}" -f s16le -ar 22.05k -ac 1 - | sudo ./pi2fm - {1} 30.0'
            .format(filename, self._freq), shell=True,
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

    '''
    Adds filename to self._queue then starts the thread to play audio if needed
    '''
    def add_to_queue(self, filename):
        self._queue.append(filename)
        print(self._queue)
        if (len(self._queue) == 1):
            _thread.start_new_thread(PiFmQueue._manage_queue, (self, ))

    '''
    Removes a filename from self._queue by filename or index
    '''
    def remove_from_queue(self, filename):
        try:
            pos = int(filename)
            self._queue.pop(pos)
        except ValueError:
            self._queue.remove(filename)
        print(self._queue)

    '''
    Checks if there are items in self._queue. Plays the 0th items if there are
    '''
    def _manage_queue(self):
        while (len(self._queue) > 0):
            self._play_sound(self._queue.pop(0))
            

if __name__ == '__main__':
    pifm = PiFmQueue(input('Frequency (MHz): '))
    while (True):
        selection = input("(E)nter or (R)emove file or (V)iew queue: ")
        if (selection == 'E'):
            pifm.add_to_queue(input('Type filename: '))
        elif (selection == 'R'):
            try:
                pifm.remove_from_queue(input('Type filename or position to remove: '))
            except Exception as ex:
                print(ex)
        elif (selection == 'V'):
            pifm.print_queue()
        else:
            print("invalid input")
