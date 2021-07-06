def telemetry_to_json(telemetry):
    json_data = []
    for i in range(len(telemetry)):
        tel = telemetry[i]
        data = {}

        if 'RPM' in tel.columns:
            data["RPM"] = tel['RPM'].tolist()

        if 'Speed' in tel.columns:
            data["Speed"] = tel['Speed'].tolist()

        if 'nGear' in tel.columns:
            data["nGear"] = tel['nGear'].tolist()

        if 'Throttle' in tel.columns:
            data["Throttle"] = tel['Throttle'].tolist()

        if 'Brake' in tel.columns:
            data["Brake"] = tel['Brake'].tolist()

        if 'DRS' in tel.columns:
            data["DRS"] = tel['DRS'].tolist()

        if 'Compound' in tel.columns:
            data["Compound"] = tel['Compound'].tolist()

        if 'TyreLife' in tel.columns:
            data["TyreLife"] = tel['TyreLife'].tolist()

        if 'TrackStatus' in tel.columns:
            data["TrackStatus"] = tel['TrackStatus'].tolist()

        if 'Distance' in tel.columns:
            data["Distance"] = tel['Distance'].tolist()

        if 'DriverAhead' in tel.columns:
            data["DriverAhead"] = tel['DriverAhead'].tolist()

        if 'Time' in tel.columns:
            data["Time"] = tel['Time'].tolist()
            for k in range(len(data["Time"])):
                data["Time"][k] = str(data["Time"][k])

        if 'SessionTime' in tel.columns:
            data["SessionTime"] = tel['SessionTime'].tolist()
            for k in range(len(data["SessionTime"])):
                data["SessionTime"][k] = str(data["SessionTime"][k])

        json_data.append(data)

    return json_data
