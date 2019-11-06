This is the Firewall assignment for Illumio

My Approach

    My solution involved keeping a sorted list of all the
port and ip address ranges in the file. For every combination
of direction and protocol, I created two lists, one for storing 
all the ranges of accepted IP addresses, and another for
storing the range of accepted ports. Each range object consists of not
only the min and max value of the range, but the row number in the csv
where this range was added, which I defined as the policy id. 
    To check if a packet was accepted, I got the ranges of 
accepted ip addresses and ranges of accepted ports (for the given direction 
and packet), and looked for all the ranges that overlapped with the packet
port and packet ip, extracting all the policy ids for each. This yields
two collections of policy ids, one for all the policy ids that have the
packet direction, protocol, and ip, and another for all policy ids that have the
packet direction, protocol, and port. If there is an overlap between these two
collections, then there is at least one row in the csv that allows all four
of these packet attributes, and therefore this packet should be accepted.
    To improve the speed of iterating through each of these lists, I
sorted them after reading the whole file, and used binary search to
find ranges that included the packet value (in accept_packet() ), as opposed
to iterating through the whole array every time.

Testing, Refinements, possible optimizations

    Due to spending a lot of the alloted time exploring alternate approaches
with binary trees, I mainly tested this by using the example csv in the prompt, as well
as another csv I made that included overlapping ranges of IP addressed and ports. I mainly looked at overlapping ranges to check that I was properly storing all the ranges and iterating through them in accept_packet(), as well as making sure that having overlapping ranges wouldn't accidently allow a port & ip address combination that should be blocked.
    A design/testing improvment would be using a testing framework and generating sample files
for load testing. Instead of having two seperate arrays for ip and ports and "joining" their policy ids on accept_packet(), I originally considered having one be nested inside the other, so that each range of ips would have a pointer to a  port range array in them, or vice versa. While this would save some time on accept_packet() by avoiding creating the sets of policy ids and finding any intersection, I was concerned that it could lead to using more overall storage, since there would another container/list object nested in each element. This is since in the case of a lot of small ranges of values, there would be a lot of these nested lists being allocated.
    Since my approach involes extracting the csv line numbers that defined the packet rules, it could
also potentially log the csv rule numbers in accept_packet(). This could help debug issues where an incorrectly
added csv line caused a packet that should have been rejected to instead be accepted.
    If I had more time, I would have tried to look into types of tree structures that would have allowed
me to "merge" ranges of values and add new values efficiently, such as maybe a range tree. This would help in the case where the csv file is too large to fit in memory and has a lot of redundant rules, or new packet rules are constantly being added. This is since with my current approach the list of all csv lines is all loaded in main memory and has to be sorted after being modified, making it not as good of a fit for an "online" algorithm.

Team preferences

My preference would be the Platform team or the Core data infrastructure layer of the Data team