__author__ = 'Hadar'
import socket
import Aes
import threading
from Rsa import *
from Crypto import *
import time
import pickle
from base64 import b64decode, b64encode
import time, sys
import struct
import pypyodbc


# region ----------   C O N S T A N T S  ------------------------------------------------------------------------------------------------
PORT = 5070
LEN_UNIT_BUF = 2048  # Min len of buffer for receive from server socket
MAX_ENCRYPTED_MSG_SIZE = 128
MAX_SOURCE_MSG_SIZE = 128
END_LINE = "\r\n"
LOCAL_ADDRESS = "0.0.0.0"
IF_CLIENT_NOT_CONNECTED = True

class server():
    def __init__(self, path):
        self.socket = socket.socket()
        self.client_keys = {}
        self.crypto = Crypto()
        self.f = open(r'\\.\pipe\myPipee', 'r+b', 0)
        self.dbcursor = self.connectdb(path)

    def connectdb(self, path):
        pypyodbc.lowercase = False
        try:
            ACCESS_DATABASE_FILE = path + r'\ComputersBasicD.accdb'
            ODBC_CONN_STR = 'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=%s;' % ACCESS_DATABASE_FILE
            conn = pypyodbc.connect(ODBC_CONN_STR)
            print 'Success connect to DB'
        except Exception,ex:
            print ex
        cur = conn.cursor()
        return cur

    def writeTGui(self, s):
        self.f.write(struct.pack('I', len(s)) + s)
        self.f.seek(0)

    def readFGui(self):
        n = struct.unpack('I', self.f.read(4))[0]
        s = self.f.read(n)
        self.f.seek(0)
        return s


    def key_exchange(self,client_socket):
        if self.crypto.private_key.can_encrypt():
            #--------------------  1 ------------------------------------------------------------------------
            # ------------  Send  server publicKey
            client_socket.send(pickle.dumps(self.crypto.private_key.publickey()) + END_LINE)
            time.sleep(0.5)
            # -----------  send  Base64 Hash of self.crypto.private_key.publickey()
            client_socket.send( b64encode(SHA256.new(pickle.dumps(self.crypto.private_key.publickey())).hexdigest()) + END_LINE)
            time.sleep(0.5)
            #--------------------  2 ------------------------------------------------------------------------
            # --------------  Wait client private key  --------------------------------------------------------
            # get Pickled private  key
            pickled_client_private_key = client_socket.recv(LEN_UNIT_BUF).split(END_LINE)[0]
            client_private_key = pickle.loads(pickled_client_private_key)

            # --------------  Wait client hash private key  ---------------------------------------------------------------------------
            # Hashing original  client private key
            calculated_hash_client_pickled_private_key = SHA256.new(pickle.dumps(client_private_key)).hexdigest()
            declared_hash_client_pickled_private_key = b64decode( client_socket.recv(LEN_UNIT_BUF).split(END_LINE)[0] )
            if calculated_hash_client_pickled_private_key != declared_hash_client_pickled_private_key:
                print "Error : hash and original"
                return

            client_private_key = RSA.importKey(client_private_key)

            ''' Due to a bug in pyCrypto, it is not possible to decrypt RSA messages that are longer than 128 byte.
                        To overcome this problem, the following code receives  the encrypted data in chunks of 128 byte.
                        We need to think how to tell the students about this behavior (another help message?)
                        And maybe we should implemented this approach in level 3 as well...
            '''

            #--------------------  3 ------------------------------------------------------------------------
            #  -------------- Receive from client in parts message
            #  -------------- encrypted by server public key info containing symmetric key and hash symmetric key encrypted by client public key
            pickled_client_key = ''
            pickled_encrypted_client_key = ''
            #   Recieve from client number of encrypted message parts
            msg_parts = client_socket.recv(LEN_UNIT_BUF).split(END_LINE)[0]
            for i in xrange(int(msg_parts)):
                # Wait from client current part of encrypt client_key
                part_pickled_encrypted_client_key = client_socket.recv(LEN_UNIT_BUF).split(END_LINE)[0]
                pickled_encrypted_client_key += part_pickled_encrypted_client_key
                # Decryption current part of encrypt client_key
                part_encrypt_client_key = pickle.loads(part_pickled_encrypted_client_key)
                part_pickled_client_key = self.crypto.private_key.decrypt(part_encrypt_client_key)
                pickled_client_key += part_pickled_client_key
            items = pickled_client_key.split('#')
            client_sym_key_original = b64decode(items[0])
            print 'Client Sym Key Original :     ' + client_sym_key_original
            print len(client_sym_key_original)
            #--------   Extract Client Hash Sym Key
            client_encrypted_hash_sym_key = b64decode(items[1])
            client_encrypted_hash_sym_key = pickle.loads(client_encrypted_hash_sym_key)

            splitted_client_encrypted_hash_sym_key = [client_encrypted_hash_sym_key[i:i+MAX_ENCRYPTED_MSG_SIZE] for i in xrange(0, len(client_encrypted_hash_sym_key), MAX_ENCRYPTED_MSG_SIZE)]
            msg_parts = len(splitted_client_encrypted_hash_sym_key)
            client_hash_sym_key = ''
            for i in xrange(int(msg_parts)):
                # Decryption current part of encrypt client_key
                part_client_encrypted_hash_sym_key = client_private_key.decrypt(splitted_client_encrypted_hash_sym_key[i])
                client_hash_sym_key += part_client_encrypted_hash_sym_key
            print 'Client Hash Sym Key  :     ' + client_hash_sym_key
            calculated_client_sym_key_original = SHA256.new(client_sym_key_original).hexdigest()
            if calculated_client_sym_key_original != client_hash_sym_key:
                print "Error : hash and original"
            return client_sym_key_original

    def sendTclient(self, csocket, data):
        encrypted_data = self.client_keys[csocket].encrypt_data(data)
        csocket.send(encrypted_data)

    def recvFclient(self, csocket):
        encrypted_data = csocket.recv(LEN_UNIT_BUF)
        data = self.client_keys[csocket].decrypt_data(encrypted_data)
        return data




    def SessionWithClient(self, csocket, Ip):
        self.client_keys[csocket].append(Ip)
        Accv = self.key_exchange(csocket)
        self.client_keys[csocket] = Accv
        AccvO = Security.Aes.AESK(Accv)
        self.client_keys[csocket] = AccvO
        UUID = self.recvFclient(csocket)
        user_name = self.recvFclient(csocket)
        os_version = self.recvFclient(csocket)
        processor = self.recvFclient(csocket)
        cpus_num = self.recvFclient(csocket)
        RAM_size = self.recvFclient(csocket)
        disk_C_size = self.recvFclient(csocket)
        self.writeTGui("New client arrives")
        self.writeTGui(Ip)
        self.writeTGui(Ip + ":UUID:"+UUID)
        self.writeTGui(Ip + ":user name:"+user_name)
        self.writeTGui(Ip + ":processor:"+processor)
        self.writeTGui(Ip + ":cpus num:"+cpus_num)
        self.writeTGui(Ip + ":RAM size:"+RAM_size)
        self.writeTGui(Ip + ":disk C size:"+disk_C_size)

    def start(self):
        self.socket.bind(('0.0.0.0', PORT))
        self.socket.listen(5)
        while True:
            client_socket, client_address = self.socket.accept()
            s = threading.Thread(target=self.SessionWithClient, args=(client_socket,client_address[0],))
            s.start()
            if(IF_CLIENT_NOT_CONNECTED == True):
                IF_CLIENT_NOT_CONNECTED = False
                c = threading.Thread(target=self.Continues())
                c.start()

    def Continues(self):
        while True:
            sockbool = True
            commend = self.readFGui()
            print commend
            Ipindex = commend.find(":")
            Ip = commend[:Ipindex]
            command = commend[Ipindex:]
            csocket = None
            for s in self.client_keys.keys():
                if self.client_keys[s][1] == Ip:
                    csocket = s
            if csocket == None:
                sockbool = False
            if sockbool == True:
                self.work(csocket,command)
            #commend will be sent to a class the will translate it to a command for the client

    def work(self,csocket,command):
        Ip = self.client_keys[csocket][1]
        print "command recieved"
        if command == "Total Using" :
            self.sendTclient(csocket,command)
            using = self.recvFclient(csocket)
            self.writeTGui(Ip + ":using:" +using)
        if command == "Get Process List":
            self.sendTclient(csocket,command)
            lengf = self.recvFclient()
            x = int(lengf)
            for i in range(x):
                PId = self.recvFclient(csocket)
                Namee = self.recvFclient(csocket)
                Usingg = self.recvFclient(csocket)
                self.dbcursor.execute(""""INSERT INTO Table1(PID \
                ,Pname,Using)\
                 VALUES ('%s', '%s', '%s')""" %(PId,Namee,Usingg))
            self.dbcursor.commit()



def task(ser,st,csocket, ip):
    print "recieved command"
    if st is not None:
        print "Refresh processes"
        ser.sendTclient(csocket,"Refresh processes list")
        lenp = ser.recvFclient(csocket)
        print lenp
        ser.writeTGui(lenp)
        for i in range(lenp):
            for l in range(3):
                n = ser.recvFclient(csocket)
                print n
                ser.writeTGui(n)
        ser.writeTGui(ser.recvFclient(csocket))
    ser.Continues(csocket,ip)


def main(argv):
    time.sleep(1)
    ser = server(argv)
    ser.start()


if __name__ == "__main__":
    main(sys.argv[1])
