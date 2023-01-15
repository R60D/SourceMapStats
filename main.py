import statistics_write
import sys
file = "output.csv"
def Read():
    if(sys.prefix == sys.base_prefix):
        print("Not running in virtual environment")
        return
    print("Running in virtual environment")
    statistics_write.Reader(file)
    input("Press Any Key To Exit...")

Read(file)