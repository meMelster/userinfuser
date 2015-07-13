### Table of Contents ###


---

# Introduction #
The client side library plugs into your server side application. The following API allows for you to register users, award points, award badges, and get widgets to render on your website.

## Init ##
To use the API, first create an UserInfuser class object which takes your account email and an API key (API keys are given out once you create an account).

```
userinfuser = UserInfuser(account_email, api_key);
```

By default, most calls are asynchronous (but you can optionally enable only synchronous calls). This means the call creates a thread to make the remote API call. This way you have little or no overhead (in terms of latency) for each call made to the userinfuser service.

## Users ##
Whenever a user logs in or signs up on your site you should call the update\_user function. This function needs a unique identifier for each user. Optionally, it takes the name which shows up on the leaderboard. You can use anything for the identifier but for the optional name be wary of making it their email address or full name due to privacy reasons.

```
//registering it this way makes them show up as Anonymous on the leaderboard
userinfuser.update_user("raj@testmail.com");

or 

//this way will show an image and their name on the leaderboard
userinfuser.update_user("raj@testmail.com", "Raj", "http://nlake44.posterous.com", "http://someurl.com/images/raj.jpg"):
```

## Awarding Points ##
Give points to a user by:
```
userinfuser.award_points("raj@testemail.com", 10, "the reason why");
```
The reason why you awarded the points is optional, but if you have enabled notification of points, then you may want to say why they got the points. You can also give negative points for bad behavior.

## Awarding Badges ##
To award a badge:
```
userinfuser.award_badge("raj@testemail.com", "badgetheme-badgename-private");

or

userinfuser.award_badge("raj@testemail.com", "badgetheme-badgename-private", "reason why", "http://link_if_they_click_the_badge.com");
```

## Widgets ##
The get\_widget function returns iframes which you embed into your website. Current widgets are
  * trophy\_case
  * leaderboard
  * points
  * rank
  * notifier
  * milestones

To get a widget:
```
userinfuser.get_widget("raj@testemail.com", "trophy_case", 500, 300);
```

The last two arguments are the height and width. They will always override the default or the setting from your account. This is because the iframe size is set on the client side. The notifier location is currently only in the bottom right corner.

## Badge Points ##
There are badges you can award only after a user has done a certain number of actions. Once the required number of badge points are attained, the badge is unlocked, and the user is notified.
To award badge points:
```
userinfuser.award_badge_points("raj@testemail.com", "mytheme-comments-private", 1, 100, "reason why", "http://link-for-badge.com");

or

userinfuser.award_badge_points("raj@testemail.com", "mytheme-referrals-private", 1, 10);

```
The first integer is the number of points you are awarding. The second is the number required to actually unlock the badge. Users are not notified when they get badge points, but they are notified if they unlock the badge. For the example above, for the user to unlock the comments badge, the API call must be made 100 times (the user made 100 comments).

# Languages #
This document describes the UserInfuser API. Current language support is:
  * Python
  * Java
  * PHP
  * Ruby

Coming Soon:
  * .NET

Ruby can be installed with the following command:
`gem install userinfuser`

The java and python client tools both work for Google App Engine applications.

## Python ##
```
class UserInfuser()
  def __init__(self, account, api_key)
  
  def get_user_data(self, user_id)
  
  def update_user(self, user_id)
  
  def award_badge(self, user_id, badge_id)
  
  def remove_badge(self, user_id, badge_id)
  
  def award_points(self, user_id, points_awarded)
  
  def award_badge_points(self, user_id, badge_id, points_awarded, points_required) 

  def get_widget(self, user_id, widget_type, height, width)

  def enable_debug(self)

  def enable_encryption(self)

  def enable_local_testing(self) 

  def only_sync_calls(self)
```
### Examples ###
```
ui = UserInfuser("test@userinfuser.com", "123-456-789")

ui.award_badge(current_user_email, "theme-badgename-private")

ui.award_points(current_user_email, 10)

# Show widgets with 100x100 size
points_widget = ui.get_widget(current_user_email, "points", 100, 100)
self.response.out.write(points_widget)

rank_widget = ui.get_widget(current_user_email, "rank", 100, 100)
self.response.out.write(rank_widget)

# Use default size of 500x300 for trophy case 
trophy_case_widget =ui.get_widget(current_user_email, "trophy_case")
self.response.out.write(trophy_case_widget)

```
## PHP ##
```
Class UserInfuser($account, $api_key)

public function get_user_data($user_id)

public function update_user($user_id)

public function award_badge($user_id, $badge_id)

public function remove_badge($user_id, $badge_id)

public function award_points($user_id, $points_awarded)

public function award_badge_points($user_id, $badge_id,  $points_awarded, $points_required)

public function get_widget($user_id, $widget_type)

public function enable_debug()

public function enable_encryption()

public function enable_local_testing()

public function only_sync_calls()
```
### Examples ###
```
$ui = new UserInfuser("test@userinfuser.com", "123-456-789");
$ui->award_badge($current_user_email, "theme-badgename-private");
$ui->award_points($current_user_email, 10);

//Show widgets with 100x100 size 
$points_widget = $ui->get_widget($current_user_email, "points", 100, 100);
print($points_widget);

$rank_widget = $ui->get_widget($current_user_email, "rank", 100, 100);
print($rank_widget);

// Use default size of 500x300 for trophy case
$trophy_case_widget = $ui->get_widget($current_user_email, "trophy_case");
print($trophy_case_widget);

```
## Java ##
```
// Constructor
public UserInfuser(final String accountId, final String apiKey)

// Class functions
public String getUserInfo(final String userId)

public boolean updateUser(final String userId)

public boolean awardBadge(final String userId, final String badgeId)

public boolean removeBadge(final String userId, final String badgeId)

public boolean awardPoints(final String userId, final int pointsAwarded)

public boolean awardBadgePoints(final String userId, final int pointsAwarded)

public String getWidget(final String userId, final WidgetType widgetType, final int height, final int width)
```
## Ruby ##
The Ruby UserInfuser gem can be installed as follows:

`gem install userinfuser`

See http://rubydoc.info/gems/userinfuser/0.9.0/UserInfuser for the  documentation.

It exposes the following API:

```
class UserInfuser
  def initialize(account, api_key, debug=false, local=false, encrypt=true, sync_all=false)

  def get_user_data(id)

  def update_user(id, name, link_to_profile, link_to_profile_image)

  def award_badge(user_id, badge_id, reason="", resource="")

  def remove_badge(user_id, badge_id)

  def award_points(user_id, points_awarded, reason="")

  def award_badge_points(user_id, badge_id, points_awarded, points_required, reason="", resource="")

  def get_widget(user_id, widget_type, height=500, width=300)
```
### Examples ###
```
require 'rubygems'
require 'userinfuser'

ui = UserInfuser.new("test@userinfuser.com", "123-456-789")

ui.award_badge(current_user_email, "theme-badgename-private")

ui.award_points(current_user_email, 10)

# Show widgets with 100x100 size
points_widget = ui.get_widget(current_user_email, "points", 100, 100)
puts points_widget

rank_widget = ui.get_widget(current_user_email, "rank", 100, 100)
puts rank_widget

# Use default size of 500x300 for trophy case 
trophy_case_widget = ui.get_widget(current_user_email, "trophy_case")
puts trophy_case_widget

```
# REST or HOWTO for Other Languages #
Let's take a look at some client side code and how requests are made:
```
def update_user(self, user_id, user_name="", link_to_profile="", link_to_profile_img=""):
    argsdict = {"apikey":self.api_key,
               "userid":user_id,
               "accountid":self.account,
               "profile_name":user_name,
               "profile_link": link_to_profile,
               "profile_img":link_to_profile_img}
    ret = None
    try:
      if self.sync_all:
        ret = self.__url_post(self.update_user_path, argsdict)
      else:
        self.__url_async_post(self.update_user_path, argsdict)
        return True
      self.debug_log("Received: %s"%ret)
    except:
      self.debug_log("Connection Error")
      if self.raise_exceptions:
        raise ui_errors.ConnectionError()
    return self.__parse_return(ret)
```

This is the python client code for making updates for users. The arguments are directly put into a post request in a straight forward manner. Asynchronous updates are required to make sure there is no additional latency. The implementation of url\_async\_post spawns a thread and ignores the returned values. If the request was synchronous, the returned value is in json, and reports if the call was successful or not. Other calls for awarding points or badges use the same method for remote procedure calls.

## Rendering Widgets ##
For getting the widgets here is the python client code:
```
def get_widget(self, user_id, widget_type, height=500, width=300):
    if widget_type not in ui_constants.VALID_WIDGETS:
      raise ui_errors.UnknownWidget()
    userhash = hashlib.sha1(self.account + '---' + user_id).hexdigest()
    self.__prefetch_widget(widget_type, user_id)
    if widget_type != "notifier":
      return "<iframe border='0' z-index:9999; frameborder='0' height='"+str(height)+"px' width='"+str(width)+"px' scrolling='no' src='" + self.widget_path + "?widget=" + widget_type + "&u=" + userhash + "&height=" +str(height) + "&width="+str(width)+"'>Sorry your browser does not support iframes!</iframe>"
    else:
      return "<div style='z-index:9999; overflow: hidden; position: fixed; bottom: 0px; right: 10px;'><iframe style='border:none;' allowtransparency='true' height='"+str(height)+"px' width='"+str(width)+"px' scrolling='no' src='" + self.widget_path + "?widget=" + widget_type + "&u=" + userhash + "&height=" +str(height) + "&width="+str(width)+"'>Sorry your browser does not support iframes!</iframe></div>"
```

Here we see the call returns a string which can be embedded into your website. If the widget is the notifier, it returns a special div wrapped around the iframe to set the zindex and positioning. There is a call to prefetch the widget which is a call to the service to make sure the widget is ready to serve in memcache when the user asks for the widget.
# Troubleshooting #
Each client library has a debug mode and also synchronous option. If for some reason you are not seeing your desired result, it is recommended you enabled both debug output and synchronous calls. By default both of these are turned off for production service.
```
from userinfuser.ui_api import UserInfuser

ui = UserInfuser("raj@cloudcaptive.com", "MY-API-KEY-HERE", sync_all=True, debug=True)
ui.update_user("testuser", "Test User")

```
and running it we see:
```
raj$ python test.py
debug is on, account: raj@cloudcaptive.com, apikey: MY-API-KEY-HERE
urllib output {"status": "success"}
Received: {"status": "success"}
```
Logging into the UI control panel I can see that this user was successfully added. Otherwise an output error would have been reported in the returned result if it was not (something like permission denied because of a bad API key).
