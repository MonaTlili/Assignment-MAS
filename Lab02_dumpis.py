            # if new_pos in parking_spaces:
            #     self.parked = True

        # else:
        #     self.parking_step += 1
        #     if  self.parking_step > self.model.random.randint(3, 6):
        #         self.parked = False
        #         self.parking_step = 0

    # def leave_parking(self):
    #     self.parked = False
    #     self.parking_step = 0
    #     self.step()

    # def step(self):
    #     if not self.parked:
    #         self.move()
    #     else:
    #         self.parking_step += 1
    #         if self.parking_step > self.model.random.randint(3, 6):
    #             self.leave_parking()
