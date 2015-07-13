## Debugging Tips ##

Here are some tips for debugging with UserInfuser:

  * Turn debugging on when using a client library for development
  * Make all request synchronous to see error messages during development
  * Make sure when doing get\_widget you are requesting the correct widget
    * trophy\_case
    * milestones
    * leaderboard
    * rank
    * notifier

If its a custom deployment, look at the error logs at appspot.com

Common Mistakes:
  * Use the the badge id for API usage, not just the name
  * Badge ids look like: theme-name-private
  * Not giving the correct API key or account email address
  * Showing a user widgets without registering that user first
    * This will result in showing the default empty widgets
    * A simple solution is to update the user before getting the widget

Conerns
  * The rank widget does not update right away as points are awarded. It is cached and only recalculated after 10 minutes have passed.