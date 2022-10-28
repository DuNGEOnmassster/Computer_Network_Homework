from random import randint
import time

class terminal:
    def __init__(self, id, args) -> None:
        self.ID = id
        self.CollisionCounter = 0
        self.successTime = 0
        self.args = args


    def get_rand_data(self):
        return randint(1,1500)


    def get_minframe(self):
        return 2 * self.args.ColisionWindow/2 * self.args.Transmission_speed
    

    def get_wait_time(self):
        return randint(1, pow(2,self.CollisionCounter)) % 10


    def check_Bus_state(self, busState):
        return busState == 0


    def sleep(self, time, is_working):
        time = int(time*10)
        for i in range(time):
            if is_working:
                print(f"Terminal:{self.ID} is busy now, Time left: {time - i} sec")
            else:
                print(f"Terminal:{self.ID} is waiting now, Time left: {time - i} sec")
        
    
    def send_message(self, Bus):
        print(f"Terminal:{self.ID} with Bus{id(Bus)}")
        while self.successTime < self.args.frame_num:
            if self.check_Bus_state(Bus[0]):
                Bus[0] |= self.ID
                print(f"Current bus: {Bus}")
                time.sleep(self.get_rand_data()%7)
                if Bus[0] == self.ID:
                    print(f"Terminal:{self.ID} send successfully")
                    Bus[0] = 0
                    self.CollisionCounter = 0
                    randtime = randint(0, 32767) % 10
                    print(f"Terminal:{self.ID} waiting {randtime} sec")
                    time.sleep(randtime)
                    self.successTime += 1
                    print(f"Terminal:{self.ID} success sent for {self.successTime} times")
                else:
                    # Collision occur
                    print(f"Terminal:{self.ID} collision occur")
                    Bus[0] = 0
                    self.CollisionCounter += 1
                    if self.CollisionCounter <= self.args.max_retrans:
                        # Reset
                        self.sleep(self.get_wait_time())
                    else:
                        print("Collision reaches upper limit, stop resending!")
                        return
        print(f"Terminal:{self.ID} send all messages!")

