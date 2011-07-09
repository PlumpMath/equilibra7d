def print_tasks():
    print
    print "# tasks"
    _tasks = sorted([t.name for t in taskMgr.getAllTasks()])
    for i, name in enumerate(_tasks, 1):
        c = _tasks.count(name)
        if c > 1:
            if i == _tasks.index(name) + 1:
                print "%02d. %s [%d]" % (i, name, c)
            else:
                # don't print anything
                pass
        else:
            print "%02d. %s" % (i, name)
    print

