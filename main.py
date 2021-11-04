from rf import RF
import asyncio


def main():
    file = open("run.csv", "w")

    def handler(frame): 
        for x in frame:
            file.write(str(x) + ", ")
        file.write("\n")

    rf = RF('COM3', 115200, handler)
    
    while(True):
        rf.read_binary()
    

if __name__ == "__main__":
   main()