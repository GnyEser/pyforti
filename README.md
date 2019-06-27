# PyForti (BETA) 

This script is firstly designed only to make user operations easier and automated on Fortigate firewalls. Tested on Fortigate 60E with v6.0.0 and Fortigate 200D v5.6.3 with Python 3.6.4. Special thanks to the **[Eczacıbaşı Bilişim](https://www.ebi.com.tr/)** company which helped me with the testing process.


**Any helpful comment, advice and contribution would be most appreciated.** 

<h3>Download</h3>

 - Open "Git Bash" and type:


`git clone https://github.com/GnyEser/pyforti.git`

<h3>Requirements</h3>

`pip install paramiko`
 
 
<h2>Example Use:</h2>


    
```python
    from pyforti import Forti
    fw = Forti(ip(str), port(int), username(str), password(str))
    conn = fw.connect()
    fw.get_user_groups(conn)  # Returns the user groups on the device as a list.
```

![Example][Visual]

[Visual]: https://raw.githubusercontent.com/GnyEser/pyforti/master/Capture.PNG "visual"

<h2>Functions:</h2>

```python
def connect(vdom = "")
```
 - Connects to the created Forti class device. If a vdom name is declared, also enters to the config mode of the vdom. Returns the paramiko connection which must be passed in every other function as an argument.
 
 
 

 ```python
 def get_users_from_group(ssh = connection, user_group(str) )
 ```


 - Returns users in the passed user group name as a python list.

  
 ```python
 def get_user_groups(ssh = connection)
 ```
  - Returns user groups' names as a python list.
  

  ```python
 def get_users(ssh = connection)
 ```
  - Returns user names as a python list.

   ```python
 def create_user(ssh = connection, username(str), password(str), tfa="disable")
 ```
  - Creates a user with the specified username, password and two factor authentication type.
  - ***tfa =** (disable, fortitoken, email, sms)*

   ```python
 def create_user_group(ssh = connection, groupname(str))
 ```
  - Creates a user group with setting firewall as the group type. Returns the user group name as a dict.

   ```python
 def add_user_to_group(ssh = connection, user_group(str), username(str))
 ```
  - Adds the specified user into the specified user group and returns the group name and user name as a dict.

   ```python
 def remove_user_from_group(ssh = connection, user_group(str), username(str))
 ```
  - Removes the specified user from the specified user group and returns the group name and user name as a dict.

  ```python
 def change_hostname(ssh = connection, hostname(str))
 ```
  - Changes the hostname of the device.

  ```python
 def check_connection(ssh = connection)
 ```
  - Checks if the connection is still up. Returns **true** if up, and **false** if down.

  ```python
 def get_arp_table(ssh = connection)
 ```
  - Returns the arp table as a string.

  ```python
 def set_dns(ssh = connection, primary(str), secondary(str))
 ```
  - Sets primary and secondary DNS addresses.

  ```python
 def show_interfaces(ssh = connection)
 ```
  - Runs 'get system interface physical' command and returns the output as a string.
 



--- 
Publish date: 27.06.2019
