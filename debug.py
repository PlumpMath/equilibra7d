import sys

# change to what is needed
WHAT_TO_DEBUG = set(['fsm', 'objects', 'managers', 'audio'])


class debug:
    """Decorator which helps to control what aspects of a program to debug
    on per-function basis. Aspects are provided as list of arguments.
    It DOESN'T slowdown functions which aren't supposed to be debugged.
    """
    colors = dict(red=1, green=2, brown=3, blue=4, purple=5, lightgray=7)
    
    def __init__(self, aspects=None):
        self.aspects = set(aspects)
    
    def color_for(self, action):
        if set(['objects', 'managers']) & self.aspects:
            color = dict(setup='green', clear='red').get(action, 'lightgray')
        elif 'fsm' in self.aspects:
            color = 'purple'
        else:
            color = 'lightgray'
        return self.colors[color]
    
    def __call__(self, f):
        if self.aspects & WHAT_TO_DEBUG:
            def newf(*args, **kwds):
                action = f.func_name
                color = self.color_for(action)
                obj = args[0].__class__.__name__
                
                print >> sys.stderr, "\033[3%dm%s %s\033[0m" % (color, obj, action)
                return f(*args, **kwds)
            newf.__name__ = f.__name__
            newf.__doc__ = f.__doc__
            return newf
        else:
            return f


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

