'''Holds the Board class for commmunicating with an SEEED Studio E5 board.
'''

import threading
import logging
import queue

from serial import Serial


class Board:

    def __init__(
        self,
        port = '/dev/ttyUSB0',   # Serial port connected to the E5 board
        downlink_callback = None,    # function this class will call if a Downlink is received
        ):

        # open up the port to communicate to the E5 board
        self.port = Serial(port, 9600, timeout=0.5)

        # remember the callback function
        self.downlink_callback = downlink_callback

        # set up a Queue to accept commands to send to E5 module
        self.cmd_q = queue.SimpleQueue()
        threading.Thread(target=self.run, daemon=True).start()

    def run(self):

        while True:

            # process any commands in the Queue
            try:
                cmd = self.cmd_q.get_nowait()
                # add an "AT+" in front and send as bytes to the board
                cmd_bytes = bytes(f'AT+{cmd.upper()}\n', 'utf-8')
                self.port.write(cmd_bytes)
            except queue.Empty:
                pass
            except Exception as err:
                logging.exception('Error accessing command queue.')

            recv_line = self.port.readline().decode('utf-8').strip()
            if len(recv_line):
                logging.debug(recv_line)
                print(recv_line)
                if 'PORT: 1; RX: "' in recv_line:
                    # this is a downlink message
                    data = recv_line.split('"')[-2]
                    print(f'Downlink message {data}')


    def add_command(self, cmd):
        """Adds a command to the queue to be sent to the E5 board.  'cmd' is a string;
        an 'AT+' is prepended to the string before being sent to the E5.
        """
        self.cmd_q.put(cmd)

    def set_data_rate(self, dr: int):
        """Changes the Data Rate of the E5 board
        """
        self.cmd_q.put(f'DR={dr}')
