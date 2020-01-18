# PyForti (BETA) 
Network automation module for FortiGate firewalls. 


This script is firstly designed to make user operations easier and automated on Fortigate firewalls. Tested on Fortigate 60E v6.0.0 and Fortigate 200D v5.6.3 with Python 3.6.4. Special thanks to **[Eczacıbaşı Bilişim](https://www.ebi.com.tr/)** company which helped me with the testing process.


**Any helpful comment, advice and contribution would be most appreciated.** 

<h3>Download</h3>

 - Open "Git Bash" and type:


`git clone https://github.com/GnyEser/pyforti.git`

<h3>Requirements</h3>

`paramiko 2.6.0`

`pip install paramiko`
 
 
<h2>Example Use:</h2>


    
```python
    from pyforti import Forti
    fw = Forti(ip(str), port(int), username(str), password(str))
    conn = fw.connect()
    fw.get_user_groups(conn)                   # Returns the user groups on the device as a list.
    fw.create_user_group(conn, "TestGroup")    # Creates a user group named "TestGroup" and returns the user group and command output as a dict.
```



<h2>Functions:</h2>

```python
conn = connect(vdom = "")
```
 - Connects to the created Forti class device. If a vdom name is declared, also enters to the config mode of the vdom. Returns the paramiko connection which must be passed in every other function as an argument.
 
 
 

 ```python
 get_users_from_group(conn, user_group(str))  # Name of the user group to get users inside.
 ```


 - Returns users in the passed user group as a python list.

  
 ```python
 get_user_groups(conn)
 ```
  - Returns each user groups' names as a python list.
  

  ```python
 get_users(conn)
 ```
  - Returns user names as a python list.

   ```python
 create_user(conn, username(str), password(str), tfa="disable")
 ```
  - Creates a user with the specified username, password and two factor authentication type.
  - ***tfa =** "disable"/ "fortitoken"/ "email"/ "sms"*

   ```python
 create_user_group(conn, groupname(str))
 ```
  - Creates a user group with setting firewall as the group type. Returns the user group name as a dict.

   ```python
 add_user_to_group(conn, user_group(str), username(str))
 ```
  - Adds the given user into the specified user group and returns the group name and user name as a dict.

   ```python
 remove_user_from_group(conn, user_group(str), username(str))
 ```
  - Removes the specified user from the specified user group and returns the group name and user name as a dict.

  ```python
 change_hostname(conn, hostname(str))
 ```
  - Changes the hostname of the device to the passed string.

  ```python
 check_connection(conn)
 ```
  - Checks if the connection is still up. Returns **true** if up, and **false** if down.

  ```python
 get_arp_table(conn)
 ```
  - Returns the arp table as a string.

  ```python
 set_dns(conn, primary(str), secondary(str))
 ```
  - Sets primary and secondary DNS addresses.

  ```python
 show_interfaces(conn)
 ```
  - Runs 'get system interface physical' command and returns the output as a string.
 



--- 
Publish date: 27.06.2019
