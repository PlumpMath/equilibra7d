def print_tasks():
    print
    print "# tasks"
    tasks = sorted([t.name for t in taskMgr.getAllTasks()])
    for i, name in enumerate(tasks, 1):
        c = tasks.count(name)
        if c > 1:
            if i == tasks.index(name) + 1:
                print "%02d. %s [%d]" % (i, name, c)
            else:
                # don't print anything
                pass
        else:
            print "%02d. %s" % (i, name)
    print

def print_events():
    print
    print "# events"
    events = sorted([e for e in messenger.getEvents()])
    for i, name in enumerate(events, 1):
        c = events.count(name)
        if c > 1:
            if i == events.index(name) + 1:
                print "%02d. %s [%d]" % (i, name, c)
            else:
                # don't print anything
                pass
        else:
            print "%02d. %s" % (i, name)
    print
