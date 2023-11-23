import os, time

import src.functions as fnc
import src.plugins.edval as edv
import src.plugins.seqta as sqt

curr_working_dir = os.getcwd()


def dm_timetable(subject: str, body: str, send: bool):
    """
    Split edval timetable using split_document()\n
    Iterate over returned names to send SEQTA DMs

    :param subject: Subject of the SEQTA DM
    :type subject: str
    :param body: Body of the SEQTA DM
    :type body: str
    :param send: True to send DM. False for testing
    :type send: bool
    """

    names, filepaths = edv.split_document()
    failures = []
    success = []

    index = 0
    for i in names:
        print("\n-------------------------------------------------------")
        print(str(index + 1) + "/" + str(len(names)))
        if (
            sqt.create_dm(name=names[index], dm_type=1) == "NotFound"
        ):  # If the function can't find a studnet return their name, add it to the list of failures and move on
            failures.append(names[index])
            index = index + 1
            continue
        else:
            success.append(names[index])
        try:
            fnc.imagecheck(r"src\assets\seqta\dm\addfiles.png")
            sqt.write_dm(
                subject=subject,
                message=body,
                filepath=[
                    curr_working_dir
                    + "\\"
                    + filepaths[index].replace(
                        "/", "\\"
                    )  # Find file that matches the name of the student
                ],
            )
        except:
            failures.append(names[index])
            send = False
        time.sleep(1)
        if send == True:
            sqt.send_dm()
        else:
            sqt.cancel_dm()
        index = index + 1

    fnc.csv_export(failures, "dm_timetable_failures.csv")
    fnc.csv_export(success, "dm_timetable_success.csv")

    return failures, success
