from collections import namedtuple

AllowedRange = namedtuple('AllowedRange','lower higher id')

# The PolicyRange is used to store ranges of accepted values along 
# with the corresponding policy ids (row # in csv) for each range.
# Upon querying a target value, PolicyRange iterates through
# all of the ranges the target is in, and returns the corresponding
# policy id for each. The updated flag is used to check if the self.ranges needs to be sorted (upon calling find_all)
class PolicyRange:
    def __init__(self):
        self.ranges = []
        self.updated = True

    def __repr__(self):
        return self.ranges.__repr__()
        

    def insert_range(self, lower, higher, policy_id): # Insert a new range just by appending it to the end of the list
        self.ranges.append(AllowedRange(lower,higher,policy_id))
        self.updated = False
    
    def _update(self):
        self.ranges.sort(key=lambda r: (r.lower, r.higher))
        self.updated = True
    
    def _find_value_range(self, target): #Do a variation of a binary search to find the left most index in self.ranges that contains target
        left, right = 0, len(self.ranges) - 1
        while left < right:
            mid = left + (right - left)//2
            mid_range = self.ranges[mid]
            if mid_range.lower <= target <= mid_range.higher:
                if mid == 0 or self.ranges[mid-1].higher < target:
                    return mid
            if mid_range.higher < target:
                left = mid + 1
            else:
                right = mid - 1
        return right

            



    def find_all(self, target):
        if not self.updated: #sort self.ranges if there have been any update since the last time find_all was called
            self._update()

        left = self._find_value_range(target) #get the range with the smallest start value that has the target, and iterate right until you get to a range that is greater than target
        found_ids = set()
        for allowed in self.ranges[left:]:
            if allowed.lower <= target <= allowed.higher:
                found_ids.add(allowed.id)
            else:
                break
        return found_ids





    
