# Base router class
from router import Router


# Class representing distance vector routers
class DVRouter(Router):
    def __init__(self, router_id):
        # Common initialization routines
        Router.__init__(self, router_id)

        # Did the distance vector change, i.e., do I need to readvertise it?
        self.dv_change = True  # This is initialized to True when this router boots up.

        # The distance vector at each node.
        # self.dv[dst] gives the current best distance to dst
        # If dst is absent in self.dv, it's equivalent to a distance of infinity.
        # Hence, we don't need to explicitly store distances of infinity.
        self.dv = dict()

    # Initialize DV at boot up
    def initialize_algorithm(self):
        # Distance vector to all neighbors of this router
        for neighbor_id in self.links:
            self.dv[neighbor_id] = self.links[neighbor_id]
            self.fwd_table[neighbor_id] = neighbor_id

        # Distance vector to this router itself
        self.dv[self.router_id] = 0
        self.fwd_table[self.router_id] = self.router_id

    def tick(self, tick):
        # If the DV changes, advertise it to every neighbor.
        # Reset the DV back to False at the end.
        if self.dv_change:
            for neighbor in self.neighbors:
                self.send(neighbor, self.dv, self.router_id)
        self.dv_change = False

    def send(self, neighbor, dv_adv, adv_router):
        neighbor.process_advertisement(dv_adv, adv_router)

    # The core logic of the algorithm goes in the process_advertisement method.
    # This method takes two arguments:
    # (1) the distance vector advertisement that it is receiving (dv_adv)
    # (2) and the router that is advertising this distance vector (adv_router)
    def process_advertisement(self, dv_adv, adv_router):
        # TODO: Implement this using the instructions below.
        # (1) Iterate through all destinations in this router's distance vector (self.dv).
        # If this destination is also in the dv_adv that you just received,
        # check if you can find a better path to the destination through adv_router
        # (2) Iterate through all destinations in the just received distance vector (dv_adv),
        # which are not in this router's current distance vector (self.dv)
        # , i.e., this router's current distance to them is infinity.
        # For such destinations, you should update the distance vector and next hop information
        # to use adv_router because the current distance is infinity.
        # (3) Make sure you update self.fwd_table[dst] to reflect the current best choice
        # of next hop to destination dst. simulator.py uses this to check your implementation.
        for distance in self.dv:
            if (distance in dv_adv and dv_adv[distance] + self.links[adv_router] < self.dv[distance]):
                upd = self.links[adv_router] + dv_adv[distance] 
                self.dv[distance] = upd
                self.fwd_table[distance] = adv_router
                self.dv_change = True

        for distance in dv_adv:
            if (distance not in self.dv):
                upd = self.links[adv_router] +  dv_adv [distance] 
                self.dv[distance] = upd
                self.fwd_table[distance] = adv_router
                self.dv_change = True

        pass

