def position_to_json(telemetry):
    json_data = {}
    # for i in range(len(telemetry)):
    #     tel = telemetry[i]
    #     data = {}
    # 
    if 'Date' in telemetry.columns:
        json_data["Date"] = telemetry['Date'].tolist()

    if 'X' in telemetry.columns:
        json_data["X"] = telemetry['X'].tolist()

    if 'Y' in telemetry.columns:
        json_data["Y"] = telemetry['Y'].tolist()

    if 'Time' in telemetry.columns:
        json_data["Time"] = telemetry['Time'].tolist()
        for k in range(len(json_data["Time"])):
            json_data["Time"][k] = str(json_data["Time"][k])

    if 'SessionTime' in telemetry.columns:
        json_data["SessionTime"] = telemetry['SessionTime'].tolist()
        for k in range(len(json_data["SessionTime"])):
            json_data["SessionTime"][k] = str(json_data["SessionTime"][k])
    # 
    #     jsonData.append(data)

    return json_data
