from pipeline import clear_names, register, summary

if __name__ == '__main__':
    print(clear_names(["  Caleb", "DAVID   "]))
    register("high")
    register("low")
    print(summary({"keyboard": 360.0, "mouse": 125.0}))