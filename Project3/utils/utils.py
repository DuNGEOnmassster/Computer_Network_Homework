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
                print(f"终端{self.ID}工作中，剩余时间：", (time - i))
            else:
                print(f"终端{self.ID}等待中，剩余时间：", (time - i))
        
    
    def send_message(self, Bus):
        print(f"terminal{self.ID} with Bus{id(Bus)}")
        while self.successTime < self.args.frame_num:
            if self.check_Bus_state(Bus[0]): # 当前总线空闲,可以发送
                Bus[0] |= self.ID
                print("现在的bus：", Bus)
                time.sleep(self.get_rand_data()%7)
                if Bus[0] == self.ID:
                    print(f"终端{self.ID}发送成功")
                    Bus[0] = 0
                    self.CollisionCounter = 0
                    randtime = randint(0, 32767) % 10
                    print(f"终端{self.ID}随机等待{randtime}sec")
                    time.sleep(randtime)
                    self.successTime += 1
                    print(f"终端{self.ID}发送成功次数：{self.successTime}")
                else:
                    # 发生冲突
                    print(f"终端{self.ID}发送时发生冲突")
                    Bus[0] = 0
                    self.CollisionCounter += 1
                    if self.CollisionCounter <= self.args.max_retrans:
                        # 退避重发
                        time.sleep(self.get_wait_time())
                    else:
                        print("冲突次数>16,发送失败")
                        return
        print(f"终端{self.ID}发送完毕")

