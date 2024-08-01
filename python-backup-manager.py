#!/usr/bin/python
#RUN SCRIPT FOR BOTH GUI AD COMMAND LINE ARGUMENT AND GIVE USERS OPTIONS TO EITHER RUN AS TKINTER OR THROUGH THE BACKEND USING COMM LINE

import os
import shutil
import time
import sys
import subprocess
import logging
import tarfile
import tkinter
from tkinter import messagebox

class backupmanager:
    def __init__(self, source_list, destination_list, ts):
        self.ts = ts
        self.source_list = source_list
        self.destination_list = destination_list


        self.windows = None
        self.txt_disc = None
        self.txt_threshold = None
        self.txt_runner = None
        self.txt_logfile_path = None
        self.txt_logfile_name = None
        self.status_label = None




    #Defining a log location function
    def log_loc(self, log_file_path, log_file_name, runner):
        try:
            log_dir = os.path.join(log_file_path, f"{runner}")
            os.makedirs(log_dir, 0o700, exist_ok=True)
            log_file = log_dir + "/" + self.ts + "_" + log_file_name
            logging.basicConfig(filename=log_file, filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO)
            logging.info(f"The logfile {log_file} has successfully been created")
        except Exception as e:
            print(f"Unable to create a logfile direcotry: {e}")




    def compress_backup(self, backup_path, compressed_file_name):
        logging.info(f"Creating a compressed backup archive: {compressed_file_name}")
        try:
            with tarfile.open(compressed_file_name, "w:gz") as tar:
                for path in backup_path:
                    if os.path.exists(path):
                        arcname=os.path.basename(path)
                        logging.info(f"Adding {path} to the compressed archive")
                        tar.add(path, arcname=arcname)
            logging.info(f"Compressed archive has successfully been created: {compressed_file_name}")
        except Exception as e:
            print(f"Unable to create compressed archive: {e}")

        


    def onprem_backup(self, source_list, destination_list, runner, ts, compress=True):
        logging.info("You selected the onpremise backup function")
        backup_path = []
        if len(self.source_list) != len(self.destination_list):
            logging.info("Error has been detected: Ensure that the source and directory list has the same number of entries")
            exit()
            
        for source, destination in zip(self.source_list, self.destination_list):
            new_dst=os.path.join(destination, runner, ts)
            backup_path.append(new_dst)
            if os.path.isfile(source):
                logging.info("Calling the file backup function")
                os.makedirs(new_dst, exist_ok=True)
                time_string1=time.localtime()
                TS1=time.strftime("%d/%m/%y_%H:%M:%S" , time_string1)
                print(f"starting the backup job at {TS1}")
                shutil.copy(source, new_dst)

                #End time variable
                time_string2=time.localtime()
                TS2=time.strftime("%d/%m/%y_%H:%M:%S" , time_string2)
                print(f"File successfully copied to {new_dst} at {TS2}")

            else:
                os.path.isdir(source)
                logging.info("Calling the drectory backup function")
                time_string1=time.localtime()
                TS1=time.strftime("%d/%m/%y_%H:%M:%S" , time_string1)
                logging.info(f"starting the backup job at {TS1}")
                shutil.copytree(source, new_dst)

                #End time variable
                time_string2=time.localtime()
                TS2=time.strftime("%d/%m/%y_%H:%M:%S" , time_string2)
                print(f"Directory successfully copied to {new_dst} at {TS1}")

        if compress:    
            compressed_file_name = f"/home/oracle/scripts/praticedir_oluwole_june25/logbackup_{self.ts}.tar.gz"
            self.compress_backup(backup_path, compressed_file_name)
        


##########################################################################################################################
###################### DISC UTILIZATION FUNCTION #########################################################################


    def disc_utilization(self, disc, threshold, source_list, destination_list, runner, ts):
        logging.info("You selected the disc utilization function")
        hostname=subprocess.getoutput('hostname')
        server_list={
                "DESKTOP-L9S01RK":"onprem_backup"
        }

        if hostname in server_list:
            if server_list[hostname] == 'onprem_backup':
                logging.info(f"HURRAY!!! {hostname} is found in the server")

                ##Checking total disc size
                total_disc_size=os.popen(f"df -h '{disc}' | egrep '{disc}' | awk '{{print $5}}' | sed 's/%//'")
                disc_used=total_disc_size.read()
                logging.info(f"The available size of {disc} is {disc_used}")
                if (int(disc_used) > threshold):
                    print("Disc has exceeded its limit: Preparing to run the backup job")
                    self.onprem_backup(source_list, destination_list, runner, ts)
                else:
                    print(f"{disc} is still within threshold")
        else:
            print("Hostname not available in the server list")



    def main_comm_line(self):

        #General variable declarat
        disc=sys.argv[1]
        threshold=int(sys.argv[2])
        runner=sys.argv[3]
        log_file_path=sys.argv[4]
        log_file_name=sys.argv[5]

        #calling log location function
        self.log_loc(log_file_path, log_file_name, runner)    

        #Listing command line arguments
        logging.info(f"The first command line argument is {disc}")
        logging.info(f"The third command line argument is {threshold}")
        logging.info(f"The fourth command line argument is {runner}")
        logging.info(f"The fifth command line argument is {log_file_path}")
        logging.info(f"The sixth command line argument is {log_file_name}")

        #Calling the disc utilization function
        self.disc_utilization(disc, threshold, source_list, destination_list, runner, ts)



##############################################################################################################################
################################ GUI FUNCTION #################################################################################


    def run_tkinter_gui(self): 

        # Creating a window using the tk function in the tkinter module
        self.window = tkinter.Tk()
        self.window.title("Backup Entry Form")

        # Create a new frame with the window
        frm_form = tkinter.Frame(relief=tkinter.SUNKEN, borderwidth=1)
        frm_form.pack(padx=10, pady=10)

        # To create label and text boxes for source directory
        lbl_disc = tkinter.Label(master=frm_form, text="Disc Name")
        # Create a text box for source directory
        self.txt_disc = tkinter.Entry(master=frm_form, width=30)
        lbl_disc.grid(row=0, column=0, sticky="e")
        self.txt_disc.grid(row=0, column=1)

        # Create label and text box for threshold
        lbl_threshold = tkinter.Label(master=frm_form, text="Set Threshold")
        self.txt_threshold = tkinter.Entry(master=frm_form, width=30)
        lbl_threshold.grid(row=1, column=0, sticky="e")
        self.txt_threshold.grid(row=1, column=1)

        # Create label and text box for runner
        lbl_runner = tkinter.Label(master=frm_form, text="Runner")
        self.txt_runner = tkinter.Entry(master=frm_form, width=30)                              
        lbl_runner.grid(row=2, column=0, sticky="e")
        self.txt_runner.grid(row=2, column=1)

        # Create label and text box for log file path
        lbl_logfile_path = tkinter.Label(master=frm_form, text="Log Path")
        self.txt_logfile_path = tkinter.Entry(master=frm_form, width=30)
        lbl_logfile_path.grid(row=3, column=0, sticky="e")
        self.txt_logfile_path.grid(row=3, column=1)

        # Create label and text box for log file name
        lbl_logfile_name = tkinter.Label(master=frm_form, text="LogFile Name")
        self.txt_logfile_name = tkinter.Entry(master=frm_form, width=30)
        lbl_logfile_name.grid(row=4, column=0, sticky="e")
        self.txt_logfile_name.grid(row=4, column=1)

        # Create a frame for buttonsfrm_button = tkinter.Frame()
        frm_button = tkinter.Frame()
        frm_button.pack(fill=tkinter.X, ipadx=5, ipady=5)

        # Status label for feedback
        self.status_label = tkinter.Label(self.window, text="")
        self.status_label.pack(pady=5)

        # The button submit function
        btn_submit = tkinter.Button(master=frm_button, text="Submit", command=self.handle_submit)
        btn_submit.pack(side=tkinter.RIGHT, ipadx=10)

        # The button cancel function
        btn_cancel = tkinter.Button(master=frm_button, text="Cancel", command=self.handle_clear)
        btn_cancel.pack(side=tkinter.RIGHT, ipadx=10)
        self.window.mainloop()


    def handle_clear(self):
        print(f"You have successfully cancelled this action")
        exit()

    def handle_submit(self):

        ####Listing the variable
        disc=self.txt_disc.get()
        threshold_str=self.txt_threshold.get()
        runner=self.txt_runner.get()
        log_file_path=self.txt_logfile_path.get()
        log_file_name=self.txt_logfile_name.get()


        self.log_loc(log_file_path, log_file_name, runner)

        if not disc or not threshold_str or not runner or not log_file_path or not log_file_name:
            status_label.config(text="All field has to be filled", fg="red")
            return

        #Listing command line arguments
        logging.info(f"The first command line argument is {disc}")
        logging.info(f"The third command line argument is {threshold_str}")
        logging.info(f"The fourth command line argument is {runner}")
        logging.info(f"The fifth command line argument is {log_file_path}")
        logging.info(f"The sixth command line argument is {log_file_name}")


        #Add integer to threshold
        try:
            threshold = int(threshold_str)
        except ValueError:
            logging.info("Error: Disc Threshold must be an integer")
            return

        ###Backup
        self.disc_utilization(disc, threshold, source_list, destination_list, runner, ts)



###################################################################################################################################################
################################################# CODE BODY #######################################################################################


if __name__ == "__main__":

    #source and destination list loop

    source_list=[
                "/home/oracle/scripts/praticedir_oluwole_june25/myfirstfile.txt",
                "/home/oracle/scripts/praticedir_oluwole_june25/newfiledir"
            ]
            

    destination_list=[
                "/home/oracle/scripts/praticedir_oluwole_june25/newfiledir2",
                "/home/oracle/scripts/praticedir_oluwole_june25/newfiledir3"
            ]

    #Time variable
    ts=time.strftime("%d%m%y%M%S" , time.localtime())
    manager = backupmanager(source_list, destination_list, ts)
    
    #Calling the gui function
    if len(sys.argv) == 2 and sys.argv[1].lower() == "gui":
        manager.run_tkinter_gui()

    #Calling the command line function    
    elif len(sys.argv) == 6:
        manager.main_comm_line()
    else:
        print("You entered a wrong number of command line argument.. Try again")
        exit()
