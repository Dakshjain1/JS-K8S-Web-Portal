# Instructions to setup & use our JS-K8S-Web-Portal

First setup an Apache web server & install Docker.  
I have setup in RHEL 8.  

```
# yum install httpd -y
# yum install docker-ce -y
# setenforce 0 // or create an SELINUX rule for apache group to access docker
- create an entry in sudoers file
# vim /etc/sudoers
...
apache	ALL=(ALL:ALL) NOPASSWD: ALL
...
# systemctl start httpd 
# systemctl enable httpd 
# systemctl start docker 
# systemctl enable docker 
```
Then put the html folder from this repo into /var/www/html
```
cp -rf ./html/*  var/www/html/
```
Put the cgi-bin folder into /var/www/cgi-bin
```
cp -rf ./cgi-bin/*  var/www/cgi-bin/
```
Apache service should be running on port 80 by default (you can change it as well)
Then easily use the site - 
```
http://IP:80/task9/k8s.html
```
Then you can use the portal to - 
* Display all pods, deployment, service
* Create pods, deployment, services
* Expose deployments
* Scale the deployment
* Delete particular/all resources
 
Rest you can explore in the images below - 

