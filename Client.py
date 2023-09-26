import socket
import threading
from time import sleep

sock = socket.socket()
addr = ("46.151.28.196", 55555)
sock.connect(addr)


my_nick = input("Input your nickname: ").encode("ascii")

chat_buffer = ""
is_ready_to_chat = False

def receiving(sock, my_nick):
    global chat_buffer, is_ready_to_chat
    while True:
        try:
            data_in = sock.recv(1024).decode("ascii")
            if data_in == "NICK":
                sock.send(my_nick)
            else:
                chat_buffer += "{}\n".format(data_in)  
                is_ready_to_chat = True              
        except:
            print("Smthg wrong happened!")
            sock.close()
            break


def sending(sock):
    global chat_buffer, is_ready_to_chat
    while True:
        if is_ready_to_chat:
            sleep(2)
            print(chat_buffer)
            chat_buffer = ""
            data_out = input("Введите сообщение: ")
            sock.send(data_out.encode("ascii"))

        

out_tread = threading.Thread(target=sending, args=(sock,))

rec_tread = threading.Thread(target=receiving, args=(sock, my_nick,))
rec_tread.start()


out_tread.start()
       

