__author__ = 'Hadar'
import socket, time
import system
import Monitor
from Monitor import *
from Rsa import *
from Aes import *
from base64 import b64encode, b64decode
import pickle

#region ----------   CONSTANTS   ---------------------------------------------------------------
SERVER_ADDRESS = '127.0.0.1'             # The default target server ip
SERVER_PORT = 5070                       # The default target server port
LEN_UNIT_BUF = 2048                      # Min len of buffer for recieve from server socket
MAX_RSA_MSG = 128                        # Maximum length of message encrypted in RSA module (pyCrypto limitation)
MAX_ENCRYPTED_MSG_SIZE = 128
END_LINE = "\r\n"                        # End of line
#endregion
#==================================================================================================





class client:
    def __init__(self):
        self.socket = socket.socket()
        self.key = Random.new().read(int(16))
        self.crypto = Crypto()
        self.Aesob = AESK(self.key)
        self.monitorc = Monitor.monitor(self)
        self.syst = system.System()
        self.syst.run()
        self.cp = system.CPU(self.monitorc)
    def key_exchange(self):
        #--------------------  1 ------------------------------------------------------------------------
        # --------------  Wait server Public_Key --------------------------------------------------------
        # get Pickled public key
        pickled_server_public_key = self.socket.recv(LEN_UNIT_BUF).split(END_LINE)[0]
        server_public_key = pickle.loads(pickled_server_public_key)
        # --------------  Wait server hash Public_Key ---------------------------------------------------------------------------
        # Hashing original Public_Key
        calculated_hash_server_pickled_public_key = SHA256.new(pickle.dumps(server_public_key)).hexdigest()
        declared_hash_server_pickled_public_key = b64decode( self.socket.recv(LEN_UNIT_BUF).split(END_LINE)[0] )
        if calculated_hash_server_pickled_public_key != declared_hash_server_pickled_public_key:
            return "Not Magic"

        #--------------------  2 ------------------------------------------------------------------------
        # ------------  Send  client private key
        self.socket.send(pickle.dumps(self.crypto.private_key.exportKey()) + END_LINE)
        time.sleep(0.5)
        # -----------  send  Base64 Hash of self.crypto.private_key
        self.socket.send( b64encode(SHA256.new(pickle.dumps(self.crypto.private_key.exportKey())).hexdigest()) + END_LINE)
        time.sleep(0.5)

        #--------------------  3 ------------------------------------------------------------------------
        # -------------- Send  encrypted by server public key info containing symmetric key and hash symmetric key encrypted by client public key ---------------------
        if self.crypto.private_key.can_encrypt():
            hash_sym_key = SHA256.new(self.key).hexdigest()
            print str(hash_sym_key)
            pickle_encrypt_hash_sym_key = pickle.dumps(self.crypto.private_key.publickey().encrypt(hash_sym_key, 32))
            message = b64encode(self.key) + "#" + b64encode( pickle_encrypt_hash_sym_key )
            print message
            splitted_pickled_message = [message[i:i+MAX_ENCRYPTED_MSG_SIZE] for i in xrange(0, len(message), MAX_ENCRYPTED_MSG_SIZE)]
            #   Sending to server number of encrypted message parts
            self.socket.send(str(len(splitted_pickled_message)) + END_LINE)
            pickled_encrypted_message = ''
            for part in splitted_pickled_message:
                part_encrypted_pickled_message = server_public_key.encrypt(part, 32)
                pickled_part_encrypted_pickled_message = pickle.dumps(part_encrypted_pickled_message)
                self.socket.send(pickled_part_encrypted_pickled_message + END_LINE)
                pickled_encrypted_message += pickled_part_encrypted_pickled_message
                time.sleep(0.5)
            print "finished key exchange"

    def send(self,data):
        encrypted_data = self.Aesob.encrypt_data(data)
        self.socket.send(encrypted_data)

    def recieve(self):
        encrypted_data = self.socket.recv(LEN_UNIT_BUF)
        data = self.Aesob.decrypt_data(encrypted_data)
        return data

    def translate(self, st):
        if (st is "Update Processes"):
            processes = self.syst.get_processes_dict()
            self.syst.create_process_handle_dict(processes)
            self.cp.run(processes)
            using = self.cp.cpu_utilization()
            processeslen = len(processes.keys())
            processeslenn = str(processeslen)
            self.syst.add_each_process_using_cpu(self.cp,processes)
            self.send(processeslenn)
            i = 0
            for item in processes:
                i = i +1
                print i
                itemm = str(item)
                self.send(itemm)
                namem = str(processes[item][0])
                self.send(namem)
                usingm = str(processes[item][2])
                self.send(usingm)
            print "finished"
            cpusin = str(self.cp.cpu_utilization())
            self.send(cpusin)
        #translate more commands in the future
        if (st == "command recieved"):
            self.send(self.cp.cpu_utilization())
    def continues(self):
        while True:
            commend = self.recieve()
            print commend
            #send to the relevant task and return the result
            self.translate(commend)


    def start(self):
        self.socket.connect((SERVER_ADDRESS, SERVER_PORT))
        self.key_exchange()
        basic_info = System.system.recieve_starting_info(self)
        for item in basic_info:
            item = str(item)
            self.send(item)
        self.continues()

clienn = client()
clienn.start()

