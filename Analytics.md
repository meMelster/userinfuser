# Introduction #

This section describes what analytics are currently supported, how they are calculated in a distributed manner, and what additional analytics are to come.

# Current Support #
  * Number of API calls made
  * Number of points awarded
  * Number of badges awarded
  * Number of badge points awarded
    * This metric gives the most information because each badge can be associated with an important metric (i.e, referrals)

# Analytics using Fantasm #
For each API call made to UserInfuser, a log is created. Every badge awarded, every point granted, every widget viewed (and so on) is logged and timestamped. Each day a background process is started to tally up the previous day's events. Google App Engine has very limited capabilities for doing complex SQL statements. They only allow for select statements (no JOINs, MERGES, COUNT functionality). To handle large quantities of logs UserInfuser uses [fantasm](http://code.google.com/p/fantasm/).

## Fantasm ##
Fantasm is a fantastic library for App Engine which allows applications to abstract away TaskQueues (background tasks in App Engine) to perform distributed processing of entities. The developer must specify a workflow as a finite state machine, and do so in YAML.

### Finite State Machine ###
Here is one of the state machines used by UserInfuser:

```
- name: CountAwardedBadges

  states:

  - name: CountAwardedBadgeInitState
    initial: True
    action: serverside.analytics.AllAccountsClass
    continuation: True
    final: True
    transitions:
    - event: peraccount
      to: PerAccountState
   
  - name: PerAccountState
    action: serverside.analytics.PerAccountClass
    continuation: True
    final: True
    transitions:
    - event: perbadge
      to: PerBadgeState

  - name: PerBadgeState
    action: serverside.analytics.PerBadgeClass
    continuation: True
    final: True
    transitions:
    - event: count
      to: CountAwardedBadgesState
    
  - name: CountAwardedBadgesState
    action: serverside.analytics.CountAwardedBadgesClass
    final: True

```

### FSM Visualization ###
Fantasm also uses the Google Chart API to visualize your state machine:
![http://i.imgur.com/alXw0.png](http://i.imgur.com/alXw0.png)

## Code Example ##
```
// Start the State Machine
context = {}
context['start_time'] = str(stripMilSecs(a_day_ago))
context['end_time'] = str(stripMilSecs(now))
fsm.startStateMachine('CountAwardedBadges', [context])
"""
Badge Award Counting State Machine
This class starts a task for each account 
"""
class AllAccountsClass(DatastoreContinuationFSMAction):
  def getQuery(self, context, obj):
    return Accounts.all()

  def execute(self, context, obj):
    if not obj['result']:
      return None
    acc = obj['result']
    if acc:
      context['account_key'] = acc.key().name()
      return "peraccount"

"""
Second state for each account's badges to count over
"""
class PerAccountClass(DatastoreContinuationFSMAction):
  def getQuery(self, context, obj):
    account_key = context['account_key']
    account_ref = accounts_dao.get(account_key)
    return Badges.all().filter('creator =', account_ref)

  def execute(self, context, obj):
    if not obj['result']:
      return None
    ii = obj['result']
    context['badgeid'] = ii.theme + '-' + ii.name + '-' + ii.permissions
    return "perbadge"

"""
Awarded Badge Counting State Machine
"""
class PerBadgeClass(DatastoreContinuationFSMAction):
  def getQuery(self, context, obj):
    start_time = datetime.datetime.strptime(context['start_time'], "%Y-%m-%d %H:%M:%S")
    end_time = datetime.datetime.strptime(context['end_time'], "%Y-%m-%d %H:%M:%S")
    return Logs.all().filter("account =", context['account_key']).filter("badgeid =", context['badgeid']).filter("event =", "notify_badge").filter("date >", start_time).filter("date <", end_time)


  def execute(self, context, obj):
    # Create a counter initialized the count to 0
    # This way we'll at least know when its a sum of 0
    # rather than having nothing to signify that it ran
    def tx():
      batch_key = context['account_key'] + '-' + \
                  context['badgeid'] + '-' + \
                  context['end_time']

      batch = BadgeBatch.get_by_key_name(batch_key)
      if not batch:
        end_time = datetime.datetime.strptime(context['end_time'], "%Y-%m-%d %H:%M:%S")
        batch = BadgeBatch(key_name=batch_key,
                       badgeid=context['badgeid'],
                       account_key=context['account_key'],
                       date=end_time)
        batch.put()
    if not obj['result']:
      return None
    db.run_in_transaction(tx)
    return "count"

"""
This class spawns a task for each log.
"""
class CountAwardedBadgesClass(FSMAction):
  def execute(self, context, obj):
    """Transactionally update our batch counter"""
    batch_key = context['account_key'] + '-' + \
                context['badgeid'] + '-' + \
                context['end_time']

    def tx():
      batch = BadgeBatch.get_by_key_name(batch_key)
      if not batch:
        # For whatever reason it was not already created in previous state
        end_time = datetime.datetime.strptime(context['end_time'], "%Y-%m-%d %H:%M:%S")
        batch = BadgeBatch(key_name=batch_key,
                       badgeid=context['badgeid'],
                       account_key=context['account_key'],
                       date=end_time)
        batch.put()
      batch.counter += 1
      batch.put()
    db.run_in_transaction(tx)
```

More notes on fantasm can be found [here](http://nlake44.posterous.com/my-notes-on-fantasm-for-google-app-engine)

# More Analytics to Come #
  * Daily user logins
  * Clicks on notifications
  * Total number of users
  * Total number of points/badges/badge points

Email support@cloudcaptive.com for additional suggestions.