def readSensor(path, ids):
    with open(path, "r") as f:
        ans = f.readlines()

    data = dict()

    try:
        first_line = ans[0].replace("\n", "")
        success = first_line.split(" ")[-1]
        if success == "YES":
            for j in range(min(len(ans)-1, len(ids)-1)):
                current_line = ans[j+1].replace("\n", "")
                if current_line[:2] != "00":
                    current_value = float(current_line.split("t=")[1])/1000
                    data[ids[j]] = current_value
    except:
        pass

    return data
