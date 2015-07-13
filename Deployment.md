# Introduction #

This wiki page describes how to run your own gamification platform using UserInfuser on AppScale. If you don't want to go through the hassle of propping it up visit http://userinfuser.com to use this platform as a paid service.

# Download The Application #

Get the latest code from [GitHub](https://github.com/nlake44/UserInfuser)


![http://upload.wikimedia.org/wikipedia/commons/thumb/7/74/AppScale_Systems_Logo.png/417px-AppScale_Systems_Logo.png](http://upload.wikimedia.org/wikipedia/commons/thumb/7/74/AppScale_Systems_Logo.png/417px-AppScale_Systems_Logo.png)
# Steps for AppScale #
This option is for those who want to host it on their own hardware (Xen, KVM, physical hardware, Eucalyptus) or on a public cloud like Amazon's EC2.
  * Setup and run AppScale: http://github.com/AppScale/appscale
  * The UserInfuser code must be modified to find and replace where you see "appspot.com" to the machine you are running it on (ip:port)
  * Deploy the application
    * appscale deploy userinfuser
    * or use the upload webpage
  * Change the client side api url to where AppScale is hosting it

If you need help setting it up, or want commercial support, contact:
community@appscale.com
<a href='Hidden comment: 
[http://code.google.com/appengine/images/appengine_lowres.png]
= Steps For Google App Engine =

* Go to appspot.com
* Sign up and select a unique application identifier
* Enable billing (optional)
* Download the SDK
* Change the application name in the code in userinfuser/serverside/constants.py and userinfuser/app.yaml
* There are some sender emails in userinfuser/serverside/signup.py that should be changed to the owner of the app"s email (currently raj at cloudcaptive.com). Grep/search for the email in the code and change it to your own.
* Upload your application to google"s infrastructure
* python appcfg.py update your-userinfuser-appname
* Change the client side api name to your app identifier
'></a>