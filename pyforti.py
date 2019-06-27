import paramiko
import time
import traceback
import logging



class Forti:

    
    def __init__(self,ip,port,username,password):
        self.ipaddress = ip
        self.ssh_pre = paramiko.SSHClient()
        self.port = port
        self.username = username
        self.password = password

    

    #   Before any configuration, we need to connect to the device via SSH using paramiko.
    def connect(self, vdom=""):
        self.ssh_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh_pre.connect(self.ipaddress,username=self.username,password=self.password,port=self.port)
        time.sleep(0.5)
        ssh = self.ssh_pre.invoke_shell()
        self.hostname = self.get_hostname(ssh)
        time.sleep(0.2)
        if not vdom == "":
            ssh.send("config global\n")
            time.sleep(0.3)
            ssh.send("config system console\n")
            time.sleep(0.3)
            ssh.send("set output standard\n")           # To make any output readable by python without pressing space
            time.sleep(0.3)
            ssh.send("end\n")
            time.sleep(0.2)
            ssh.send("end\n")
            time.sleep(0.3)
            ssh.send("config vdom\n")
            time.sleep(0.3)
            ssh.send("edit {}\n".format(vdom))          # Entering config mode of the requested vdom
            time.sleep(0.3)
            return ssh
        if vdom == "":
            ssh.send("config system console\n")
            time.sleep(0.3)
            ssh.send("set output standard\n")
            time.sleep(0.3)
            ssh.send("end\n")
            return ssh
        #ssh.send("end\n")
        else:
            return(ssh)


    # Should only be used when connection established first by connect() function.
    def get_hostname(self,ssh):
        raw_output = ssh.recv(65535)
        output = raw_output.decode("utf-8")
        output = output.replace("#","")
        return output

    def get_users_in_group(self,ssh,user_group):
        try:
            ssh.send("config user group\n")
            time.sleep(0.4)
            command = "get " + user_group 
            ssh.send(command + "\n")
            time.sleep(0.2)
            raw_output = ssh.recv(65535)
            output = self.clean_output(output=raw_output, command=command)
            raw_users = output.splitlines()
            users = list()
            for i in raw_users:
                if "member" in i:
                    raw_users = i.split(":")[1]
                    break
            for x in range(len(raw_users.split('"'))):
                if x%2 == 1:
                    users.append(raw_users.split('"')[x])
            ssh.send("end\n")
            time.sleep(0.2)
            return users
        except Exception as e:
            logging.error(traceback.format_exc())
            error_message = "Command failed."
            return error_message

    def get_user_groups(self,ssh):
        try:
            command = "get user group"
            ssh.send(command)
            ssh.send("\n")
            time.sleep(0.3)
            raw_output = ssh.recv(65535)
            #print(raw_output)
            output = self.clean_output(output=raw_output, command=command)
            raw_user_groups = output.splitlines()
            user_groups = list()
            for i in raw_user_groups:
                if "name:" in i:
                    user_groups.append((i.replace("name:","")).strip())
            return user_groups

        except:
            error_message = "Command failed."
            return error_message

    def get_users(self,ssh):
        try:
            command="get user local"
            ssh.send(command + "\n")
            time.sleep(0.3)
            raw_output = ssh.recv(65535)
            #print(raw_output)
            output = self.clean_output(output=raw_output, command=command)
            #print(output)
            raw_users = output.splitlines()
            users = list()
            for i in raw_users:
                if "name:" in i:
                    users.append((i.replace("name:","")).strip())
            return users
        except:
            error_message = "Command failed."
            return error_message


    def disconnect(self):
        self.ssh_pre.close()


    def create_user(self,ssh,username,password,tfa="disable"):
        new_user = { "username":username , "password":password, "two-factor-auth":tfa}
        try:
            ssh.send("config user local\n")
            time.sleep(0.6)
            ssh.send("edit {}\n".format(username))
            time.sleep(0.6)
            ssh.send("set type password\n")
            time.sleep(0.6)
            ssh.send("set passwd {}\n".format(password))
            time.sleep(0.6)
            if tfa == "disable" or tfa == "fortitoken" or tfa == "email" or tfa == "sms":
                ssh.send("set two-factor {}\n".format(tfa))
                time.sleep(0.6)
            ssh.send("end\n")
            time.sleep(0.6)
            
            return(new_user)
        except:
            error_message = "User creation failed."
            return error_message

    def create_user_group(self,ssh,groupname):
        new_user_group={"user_group_name":groupname}
        try:
            ssh.send("config user group\n")
            time.sleep(0.5)
            ssh.send("edit {}\n".format(groupname))
            output = str(ssh.recv(1024))
            #print(output)
            time.sleep(0.5)
            ssh.send("set group type firewall \n")
            time.sleep(0.5)
            ssh.send("end\n")
            time.sleep(0.5)
            return [output, new_user_group]
        except:
            error_message = "User addition failed."
            return error_message


    def add_user_to_group(self,ssh,user_group,username):
        user_and_group= { "user_group":user_group , "username":username }
        try:
            ssh.send("config user group\n")
            time.sleep(0.6)
            ssh.send("edit {}\n".format(user_group))
            time.sleep(0.6)
            ssh.send("append member {}\n".format(username))
            time.sleep(0.6)
            ssh.send("end\n")
            time.sleep(0.6)
            return(user_and_group)
        except:
            error_message = "User addition failed."
            return error_message
            

    def remove_user_from_group(self,ssh,user_group,username):
        user_and_group= { "user_group":user_group , "username":username }
        try:
            ssh.send("config user group\n")
            time.sleep(0.6)
            ssh.send("edit {}\n".format(user_group))
            time.sleep(0.6)
            ssh.send("unselect member {}\n".format(username))
            time.sleep(0.6)
            ssh.send("end\n")
            time.sleep(0.6)
            return(user_and_group)
        except:
            error_message = "User removal failed."
            return error_message


    def change_hostname(self, ssh, hostname):
        try:
            ssh.send("config system global\n")
            time.sleep(0.6)
            ssh.send("set hostname {}\n".format(hostname))
            time.sleep(0.6)
            ssh.send("end\n")
            time.sleep(0.8)
            self.hostname = hostname
            return hostname
        except:
            error_message = "Hostname change failed."
            return error_message

    def check_connection(self,ssh):
        status = ssh.__repr__()
        if "(open)" in status:
            print("Connection is up...")
            return True
        else:
            print("Connection is down...")
            return False


    # Clean output to be more readable.
    def clean_output(self,output,command):
        output = output.decode("utf-8")
        output = output.replace(self.hostname,"")
        output = output.split(command)[1]
        return output

    def get_arp_table(self,ssh):
        try:
            command = "get system arp"
            ssh.send(command)
            ssh.send("\n")
            time.sleep(0.6)
            raw_output = ssh.recv(65535)
            output = self.clean_output(output=raw_output,command=command)
            
            return output
        except:
            error_message = "Command failed."
            return error_message
        
            
    def set_dns(self, ssh, primary, secondary):
        dns_addresses = { "primary":primary, "secondary":secondary }
        try:
            ssh.send("config system dns\n")
            time.sleep(0.6)
            ssh.send("set primary {}\n".format(primary))
            time.sleep(0.6)
            ssh.send("set secondary {}\n".format(secondary))
            time.sleep(0.6)
            ssh.send("end\n")
            time.sleep(0.6)
            return dns_addresses
        except:
            error_message = "Command failed."
            return error_message

    def show_interfaces(self,ssh):
        try:
            command = "get system interface physical"
            ssh.send(command)
            ssh.send("\n")
            time.sleep(0.6)
            raw_output = ssh.recv(65535)
            output = self.clean_output(output=raw_output,command=command)
           
            return output
        except:
            error_message = "Command failed."
            return error_message
