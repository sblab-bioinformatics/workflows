<!-- MarkdownTOC -->

- [Installing rstudio-server on group server](#installing-rstudio-server-on-group-server)
    - [Install rstudio-server](#install-rstudio-server)
    - [Configuration](#configuration)
    - [Accessing rstudio-server](#accessing-rstudio-server)

<!-- /MarkdownTOC -->


Installing rstudio-server on group server
=========================================

We want to make [Rstudio](https://www.rstudio.com/) available on our group server.
Best option is to have a Rstudio run as a server. In this way, anybody with a user account on our
server can access Rstudio from any web browser. (Provided your at CI or you can connect 
via VPN from outside of course).

Install rstudio-server
----------------------

At time of this writing our server runs CentOS 6. 

Rstudio-server was downloaded from https://www.rstudio.com/products/rstudio/download-server/ 
and installed as:

```
ssh sblab-srv001
wget https://download2.rstudio.org/rstudio-server-rhel-1.0.44-i686.rpm
sudo yum install --nogpgcheck rstudio-server-rhel-1.0.44-i686.rpm
```

Configuration
-------------

It appears that the following change is required to allow users to login:

```
sudo cp /etc/pam.d/login /etc/pam.d/rstudio
```

See also [Incorrect or invalid username/password](https://support.rstudio.com/hc/en-us/community/posts/200659796-Error-Incorrect-or-invalid-username-password).

We also need to open the rstudio port (8787): 

```
sudo iptables -A INPUT -p tcp --dport 8787 -j ACCEPT

## Make the change permanent:
/sbin/service iptables save

sudo cat /etc/sysconfig/iptables
```

Accessing rstudio-server
------------------------

Now, any user with access to `sblab-srv001` can access rstudio with his/her username and password from: http://10.20.192.25:8787

(Where _10.20.192.25_ is the address of `sblab-srv001`)

<img src=pics/rstudio-server-login.png width=600>

<img src=pics/rstudio-front.png width=600>

