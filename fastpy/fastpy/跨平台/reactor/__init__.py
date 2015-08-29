import select
import sys
use_mod = None

if 'epoll' in select.__dict__:
    print "use epoll"
    use_mod = 'epoll'
    from epollreactor import EpollReactor as Reactor
elif 'kqueue' in select.__dict__:
    print "use kqueue"
    use_mod = 'kqueue'
    from kqueuereactor import KqueueReactor as Reactor
elif 'poll' in select.__dict__:
    print "use poll"
    use_mod = 'poll'
    from pollreactor import PollReactor as Reactor
elif 'select' in select.__dict__:
    print "use select"
    use_mod = 'select'
    from selectreactor import SelectReactor as Reactor
else:
    print "There is no reactor can be used."
    sys.exit(1)
