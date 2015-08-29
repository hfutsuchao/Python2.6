names = locals()
for i in xrange(1, 101):
    names['linuxany%s' % i] = i

locals()['abc'] = 2

for i in xrange(1, 101):
    print names['linuxany'+str(i)]