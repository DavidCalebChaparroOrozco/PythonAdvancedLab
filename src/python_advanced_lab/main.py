from python_advanced_lab.pipeline import clear_names, register, summary

def main() -> None:
    print(clear_names(["  Caleb", "DAVID   "]))
    register("high")
    register("low")
    print(summary({"keyboard": 360.0, "mouse": 125.0}))

if __name__ == '__main__':
    main()
