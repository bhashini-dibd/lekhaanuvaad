import datetime
import json
import shutil
import threading
import pandas as pd
import pytz
from models import CustomResponse, Status, jud_stats
from flask import request, make_response
from utilities import MODULE_CONTEXT
from anuvaad_auditor.loghandler import log_info, log_exception
import config
import os
from utilities import (
    write_to_csv,
    org_level_csv,
    write_to_csv_user,
    generate_email_notification,
    send_email,
    write_to_csv_user_daily_crn
)
import uuid
import requests

# from flask_mail import Mail, Message
# from flask import render_template
IST = pytz.timezone("Asia/Kolkata")
from flask import Flask, jsonify
from email.mime.base import MIMEBase
from email import encoders


app = Flask(__name__, template_folder="../templates")

# app.config.update(config.MAIL_SETTINGS)
# creating an instance of Mail class
# mail=Mail(app)

stats = jud_stats()
usr_collection, ch_collection = stats.mongo_connection()


@app.route(config.API_URL_PREFIX + "/anuvaad-data", methods=["POST"])
def FetchJudgementCount():
    body = request.get_json()

    def FetchJudgementCountRole_org_Wise():
        log_info("FetchJudgementCount api called", MODULE_CONTEXT)
        filename = uuid.uuid4().hex
        file_name1 = str(filename)[:-10] + "_JUD_STATS1" + ".csv"
        file_name2 = str(filename)[:-10] + "_JUD_STATS2" + ".csv"
        file_save = str(filename)[:-10] + "_JUD_Org_level_Statistics.csv"
        keys = body.keys()
        if "config" in keys and body.get("config") == "cron":
            if not os.path.exists(
            config.DOWNLOAD_FOLDER + "/" + config.DAILY_CRON_FILE_NAME1
        ) and not os.path.exists(config.DOWNLOAD_FOLDER + "/" + config.DAILY_CRON_FILE_NAME2):
                shutil.copyfile(
                    config.DOWNLOAD_FOLDER + "/" + config.backup_file_1,
                    config.DOWNLOAD_FOLDER + "/" + config.DAILY_CRON_FILE_NAME1,
                )
                shutil.copyfile(
                    config.DOWNLOAD_FOLDER + "/" + config.backup_file_2,
                    config.DOWNLOAD_FOLDER + "/" + config.DAILY_CRON_FILE_NAME2,
                )
                log_info(
                    f"files copied from weekly cron to daily cron {config.backup_file_1,config.backup_file_2}",
                    MODULE_CONTEXT,
                )
                get_trans_user_data_from_db_daily_day_crn()
            # get_trans_user_data_from_db_weekly_crn()
        elif "config" in keys and body.get("config") == "copy":
            copy_cron_csv()
        elif body.get("org"):
            org = body["org"]
            role = body["role"]
            email = body["email"]
            user_docs = stats.get_user_role_org_wise(usr_collection, role, org)
            log_info(
                f"Data returned from {config.USER_COLLECTION} collection",
                MODULE_CONTEXT,
            )
        elif body.get("role"):
            role = body["role"]
            email = body["email"]
            user_docs = stats.get_user_role_wise(usr_collection, role)
            log_info(
                f"Data returned from {config.USER_COLLECTION} collection",
                MODULE_CONTEXT,
            )
        elif "config" in keys and body.get("config") == "remove":
            if os.path.exists(config.DOWNLOAD_FOLDER + "/" + config.DAILY_CRON_FILE_NAME1):
                os.remove(config.DOWNLOAD_FOLDER + "/" + config.DAILY_CRON_FILE_NAME1)
            if os.path.exists(config.DOWNLOAD_FOLDER + "/" + config.DAILY_CRON_FILE_NAME2):
                os.remove(config.DOWNLOAD_FOLDER + "/" + config.DAILY_CRON_FILE_NAME2)
            else: 
                return {"msg":"already deleted"}
        try:
            if "config" in keys:
                pass
            else:
                from_date, end_date = stats.get_time_frame(body)
                for doc in user_docs:
                    log_info(f'fetching details for {doc["_id"]} users', MODULE_CONTEXT)
                    for user in doc["users"]:
                        ch_docs = stats.fetch_data_machine_trans_tokenised(
                            ch_collection, user, from_date, end_date
                        )
                        saved_docs = stats.fetch_data_user_trans_tokenized(
                            ch_collection, user, from_date, end_date
                        )
                        log_info(
                            f'Details collected for for userID : {user}, in org {doc["_id"]} ',
                            MODULE_CONTEXT,
                        )
                        ch_docs = [x for x in ch_docs]
                        write_to_csv(
                            ch_docs, doc["_id"], (config.DOWNLOAD_FOLDER + "/" + file_name1)
                        )
                        write_to_csv(
                            [x for x in saved_docs],
                            doc["_id"],
                            (config.DOWNLOAD_FOLDER + "/" + file_name2),
                        )

                if type(email) == list:
                    users = email
                else:
                    users = [email]

                if os.path.exists(
                    config.DOWNLOAD_FOLDER + "/" + (file_name1 and file_name2)
                ):
                    org_level_csv(
                        file_save,
                        (config.DOWNLOAD_FOLDER + "/" + file_name1),
                        (config.DOWNLOAD_FOLDER + "/" + file_name2),
                    )
                    out = CustomResponse(
                        Status.SUCCESS.value, {"files": [file_name1, file_name2]}
                    )
                    # with app.app_context():
                    file_name1 = config.DOWNLOAD_FOLDER + "/" + file_name1
                    file_name2 = config.DOWNLOAD_FOLDER + "/" + file_name2
                    file_save = config.DOWNLOAD_FOLDER + "/" + file_save
                    files = [file_name1, file_name2, file_save]
                    log_info(
                        "Generating email notification for found data !!!!", MODULE_CONTEXT
                    )
                    msg = generate_email_notification(users, "Data Generated Successfully")
                    for i, j in enumerate(files):
                        with open(j, "rb") as content_file:
                            content = content_file.read()
                            msg.add_attachment(
                                content,
                                maintype="application",
                                subtype="csv",
                                filename=j.split("/")[-1],
                            )

                        # using smtp lib
                        # attach_file = open(j, "rb")  # Open the file as binary mode
                        # payload = MIMEBase("application", "octate-stream")
                        # payload.set_payload((attach_file).read())
                        # encoders.encode_base64(payload)  # encode the attachment
                        # # add payload header with filename
                        # payload.add_header(
                        #     "Content-Disposition",
                        #     "attachment",
                        #     filename=str(j.split("/")[-1]),
                        # )
                        # msg.attach(payload)
                    send_email(msg)
                    log_info(f"Generated alert email ", MODULE_CONTEXT)
                    log_info(
                        "filenames :{},{} ".format(file_name1, file_name2), MODULE_CONTEXT
                    )
                else:
                    log_info(
                        "files : {} and {} not found".format(file_name1, file_name2),
                        MODULE_CONTEXT,
                    )
                    msg = generate_email_notification(
                        users,
                        "could not get the data either role or org given is not present in the system please check your input and try again",
                    )
                    send_email(msg)

        except Exception as e:
            log_exception(
                "Error in FetchJudgementCount: {}".format(e), MODULE_CONTEXT, e
            )
            status = Status.SYSTEM_ERR.value
            status["message"] = str(e)
            out = CustomResponse(status, None)
            return out.getres()

    threading.Thread(target=FetchJudgementCountRole_org_Wise).start()
    out = CustomResponse(
        Status.ACCEPTED.value,
        {"msg": "please check your email after some time for requested Stats"},
    )
    return out.getres()


@app.route(config.API_URL_PREFIX + "/anuvaad-data/user", methods=["POST"])
def FetchJudgementCount_user_wise():
    body = request.get_json()

    def FetchJudgementCountRole_user_org_Wise():
        log_info("FetchJudgementCount api called", MODULE_CONTEXT)
        filename = uuid.uuid4().hex
        file_name1 = str(filename)[:-10] + "_USER_WISE_JUD_STATS1" + ".csv"
        file_name2 = str(filename)[:-10] + "_USER_WISE_JUD_STATS2" + ".csv"
        file_save = str(filename)[:-10] + "_USER_WISE_JUD_Org_level_Statistics.csv"

        if body.get("email"):
            email = body["email"]
            user_docs = stats.get_all_users_active_inactive(usr_collection)
            log_info(
                f"Data returned from {config.USER_COLLECTION} collection",
                MODULE_CONTEXT,
            )
        try:
            from_date, end_date = stats.get_time_frame(body)
            for doc in user_docs:
                log_info(f"fetching details for {doc} userID", MODULE_CONTEXT)
                ch_docs = stats.fetch_data_for_userwise_trans_tokenized(
                    ch_collection, doc, from_date, end_date
                )
                saved_docs = stats.fetch_data_for_userwise_trans_user_tokenized(
                    ch_collection, doc, from_date, end_date
                )
                log_info(f"Details collected for for userID : {doc} ", MODULE_CONTEXT)
                ch_docs = [x for x in ch_docs]
                write_to_csv_user(ch_docs, (config.DOWNLOAD_FOLDER + "/" + file_name1))
                write_to_csv_user(
                    [x for x in saved_docs], (config.DOWNLOAD_FOLDER + "/" + file_name2)
                )

            if type(email) == list:
                users = email
            else:
                users = [email]

            if os.path.exists(
                config.DOWNLOAD_FOLDER + "/" + (file_name1 and file_name2)
            ):
                # org_level_csv_user(config.DOWNLOAD_FOLDER+"/"+file_save,(config.DOWNLOAD_FOLDER+'/'+file_name1),(config.DOWNLOAD_FOLDER+'/'+file_name2))
                out = CustomResponse(
                    Status.SUCCESS.value, {"files": [file_name1, file_name2]}
                )
                # with app.app_context():
                file_name1 = config.DOWNLOAD_FOLDER + "/" + file_name1
                file_name2 = config.DOWNLOAD_FOLDER + "/" + file_name2
                # file_save = config.DOWNLOAD_FOLDER+'/'+file_save
                files = [file_name1, file_name2]
                log_info(
                    "Generating email notification for found data !!!!", MODULE_CONTEXT
                )
                # tdy_date = datetime.now(IST).strftime("%Y:%m:%d %H:%M:%S")
                msg = generate_email_notification(users, "Data Generated Successfully")
                for i, j in enumerate(files):
                    with open(j, "rb") as content_file:
                        content = content_file.read()
                        msg.add_attachment(
                            content,
                            maintype="application",
                            subtype="csv",
                            filename=j.split("/")[-1],
                        )
                send_email(msg)
                log_info(f"Generated alert email ", MODULE_CONTEXT)
                log_info(
                    "filenames :{},{} ".format(file_name1, file_name2), MODULE_CONTEXT
                )
            else:
                log_info(
                    "files : {} and {} not found".format(file_name1, file_name2),
                    MODULE_CONTEXT,
                )
                msg = generate_email_notification(
                    users,
                    "could not get the data either role or org given is not present in the system please check your input and try again",
                )
                send_email(msg)
                log_info(f"Generated alert email ", MODULE_CONTEXT)

        except Exception as e:
            log_exception(
                "Error in FetchJudgementCount: {}".format(e), MODULE_CONTEXT, e
            )
            status = Status.SYSTEM_ERR.value
            status["message"] = str(e)
            out = CustomResponse(status, None)
            return out.getres()

    threading.Thread(target=FetchJudgementCountRole_user_org_Wise).start()
    out = CustomResponse(
        Status.ACCEPTED.value,
        {"msg": "please check your email after some time for requested Stats"},
    )
    return out.getres()


# no of documents count wrt to src and tgt language with org.
@app.route(config.API_URL_PREFIX + "/anuvaad-data/lang_count", methods=["GET", "POST"])
def anuvaad_chart_org_doc():
    body = request.get_json()
    if "env" in body.keys():
        url = generate_url(config.jud, "lang_count")
        headers = headers = {"Content-Type": "application/json"}
        payload = json.dumps(
            {
                "src_lang": body["src_lang"],
            }
        )
        datas = requests.post(url, data=payload, headers=headers)
        datas = datas.json()
        return datas
    result, status = stats.file_validation()
    try:
        if status == False:
            return result
        else:
            (
                total_docs,
                total_documemt_sentence_count,
                total_verified_sentence_count,
                keyss,
            ) = stats.lang_count(result, body)
            response = make_response(
                jsonify(
                    {
                        "data": {
                            "total_document_sentence_count": int(
                                total_documemt_sentence_count
                            ),
                            "total_verified_sentence_count": int(
                                total_verified_sentence_count
                            ),
                            "total_documents": int(total_docs),
                            "language_counts": keyss,
                        }
                    }
                ),
                200,
            )
            response.headers["Content-Type"] = "application/json"
            return response
            # out = CustomResponse(
            #     Status.ACCEPTED.value,
            #     {
            #         "total_document_sentence_count": int(total_documemt_sentence_count),
            #         "total_verified_sentence_count": int(total_verified_sentence_count),
            #         "total_documents": int(total_docs),
            #         "language_counts": keyss,
            #     },
            # )
            # return out.getres()

    except Exception as e:
        log_exception("Error in FetchJudgementCount: {}".format(e), MODULE_CONTEXT, e)
        status = Status.SYSTEM_ERR.value
        status["message"] = str(e)
        out = CustomResponse(status, None)
        return out.getres()


def generate_url(url_pre, end_point):
    url_modified = url_pre + "/anuvaad-metrics/anuvaad-data/" + end_point
    return url_modified


# no of documents wrt org having src and tgt lang
@app.route(config.API_URL_PREFIX + "/anuvaad-data/doc_count", methods=["POST", "GET"])
def anuvaad_chart_lang_org():
    if request.method == "POST":
        url = generate_url(config.jud, "doc_count")
        data = requests.get(url)
        data = data.json()
        return data
    result, status = stats.file_validation()
    if status == False:
        return result
    else:
        (
            total_docs,
            total_documemt_sentence_count,
            total_verified_sentence_count,
            keyss,
        ) = stats.doc_count(result)
        out = CustomResponse(
            Status.SUCCESS.value,
            {
                "total_document_sentence_count": int(total_documemt_sentence_count),
                "total_verified_sentence_count": int(total_verified_sentence_count),
                "total_documents": int(total_docs),
                "language_counts": keyss,
            },
        )
        return out.getres()


@app.route(
    config.API_URL_PREFIX + "/anuvaad-data/verified_count", methods=["POST", "GET"]
)
def anuvaad_chart_verfied_sentence():
    # body = request.get_json()
    if request.method == "POST":
        url = generate_url(config.jud, "verified_count")
        data = requests.get(url)
        data = data.json()
        return data
    result, status = stats.file_validation()
    try:
        if status == False:
            return result
        else:
            (
                total_docs,
                total_documemt_sentence_count,
                total_verified_sentence_count,
                keyss,
            ) = stats.verified_doc(result)
            out = CustomResponse(
                Status.SUCCESS.value,
                {
                    "total_document_sentence_count": int(total_documemt_sentence_count),
                    "total_verified_sentence_count": int(total_verified_sentence_count),
                    "total_documents": int(total_docs),
                    "language_counts": keyss,
                },
            )
            return out.getres()
            # return jsonify({'msgg':keyss})
    except Exception as e:
        log_exception("Error in FetchJudgementCount: {}".format(e), MODULE_CONTEXT, e)
        status = Status.SYSTEM_ERR.value
        status["message"] = str(e)
        out = CustomResponse(status, None)
        return out.getres()


@app.route(config.API_URL_PREFIX + "/anuvaad-data/languages", methods=["POST", "GET"])
def dropdown_lang():
    supported_languages = "./models/language.json"
    with open(supported_languages, "r") as f:
        data = json.load(f)
    out = CustomResponse(Status.SUCCESS.value, data)
    return out.getres()


def copy_cron_csv():
    log_info("fetch data started", MODULE_CONTEXT)
    # filename = uuid.uuid4().hex
    daily_cron_file_name1 = config.DAILY_CRON_FILE_NAME1
    daily_cron_file_name2 = config.DAILY_CRON_FILE_NAME2
    weekly_cron_file_name1 = config.WEEKLY_CRON_FILE_NAME1
    weekly_cron_file_name2 = config.WEEKLY_CRON_FILE_NAME2
    # file_save = str(filename)[:-10]+'_USER_WISE_JUD_Org_level_Statistics.csv'
    if os.path.exists(
        config.DOWNLOAD_FOLDER + "/" + weekly_cron_file_name1 ) and os.path.exists(config.DOWNLOAD_FOLDER + "/" + weekly_cron_file_name2):
        if not os.path.exists(
            config.DOWNLOAD_FOLDER + "/" + daily_cron_file_name1
        ) and not os.path.exists(config.DOWNLOAD_FOLDER + "/" + daily_cron_file_name2):
            shutil.copyfile(
                config.DOWNLOAD_FOLDER + "/" + weekly_cron_file_name1,
                config.DOWNLOAD_FOLDER + "/" + daily_cron_file_name1,
            )
            shutil.copyfile(
                config.DOWNLOAD_FOLDER + "/" + weekly_cron_file_name2,
                config.DOWNLOAD_FOLDER + "/" + daily_cron_file_name2,
            )
            data = "files copied"
            log_info(f"{data}", MODULE_CONTEXT)
        else :
            data = "Files Already in Directory"
            log_info(f"{data}", MODULE_CONTEXT)
    else:
        data = "Files Not found in Directory"
        log_info(f"{data}", MODULE_CONTEXT)

    return data


def get_trans_user_data_from_db_weekly_crn():
    users = config.EMAIL_NOTIFIER
    log_info("fetch data started", MODULE_CONTEXT)
    # filename = uuid.uuid4().hex
    weekly_cron_file_name1 = config.WEEKLY_CRON_FILE_NAME1
    weekly_cron_file_name2 = config.WEEKLY_CRON_FILE_NAME2
    daily_cron_file_name1 = config.DAILY_CRON_FILE_NAME1
    daily_cron_file_name2 = config.DAILY_CRON_FILE_NAME2
    # file_save = str(filename)[:-10]+'_USER_WISE_JUD_Org_level_Statistics.csv'
    if os.path.exists(
        config.DOWNLOAD_FOLDER + "/" + weekly_cron_file_name1
    ) and os.path.exists(config.DOWNLOAD_FOLDER + "/" + weekly_cron_file_name2):
        os.remove(config.DOWNLOAD_FOLDER + "/" + weekly_cron_file_name1)
        os.remove(config.DOWNLOAD_FOLDER + "/" + weekly_cron_file_name2)
        os.remove(config.DOWNLOAD_FOLDER + "/" + daily_cron_file_name1)
        os.remove(config.DOWNLOAD_FOLDER + "/" + daily_cron_file_name2)
    else:
        msg = generate_email_notification(
            users, "could not get the data files not found"
        )
        send_email(msg)
        log_info(f"Generated alert email scheduler files not found ", MODULE_CONTEXT)
    user_docs = stats.get_all_users_active_inactive(usr_collection)
    log_info(
        f"Data returned from user {config.USER_COLLECTION} collection", MODULE_CONTEXT
    )
    try:
        from_date, end_date = stats.get_time_frame_for_analytics()
        for doc in user_docs:
            # print(doc)
            # log_info(f'fetching details for {doc} userID',MODULE_CONTEXT)
            # done = 0
            # while True:
            #     try:
            ch_docs = stats.fetch_data_for_language_trans_tokenized_for_scheduer_only(
                ch_collection, doc, from_date, end_date
            )
            saved_docs = stats.fetch_data_for_userwise_trans_user_tokenized(
                ch_collection, doc, from_date, end_date
            )
            # log_info(f'Details collected for for userID : {doc} ',MODULE_CONTEXT)
            write_to_csv_user(
                [x for x in ch_docs],
                (config.DOWNLOAD_FOLDER + "/" + weekly_cron_file_name1),
            )
            write_to_csv_user(
                [x for x in saved_docs],
                (config.DOWNLOAD_FOLDER + "/" + weekly_cron_file_name2),
            )
            #         done = 1
                    
            #     except Exception as e:
            #         log_exception(
            #     "error in fetching the data : {}".format(str(e)),
            #     MODULE_CONTEXT,
            #     e,
            # )
            #     if done == 1:
            #         break
        log_info(
            f"Data written into files {weekly_cron_file_name1,weekly_cron_file_name2}",
            MODULE_CONTEXT,
        )
        if not os.path.exists(
            config.DOWNLOAD_FOLDER + "/" + daily_cron_file_name1
        ) and not os.path.exists(config.DOWNLOAD_FOLDER + "/" + daily_cron_file_name2):
            shutil.copyfile(
                config.DOWNLOAD_FOLDER + "/" + weekly_cron_file_name1,
                config.DOWNLOAD_FOLDER + "/" + daily_cron_file_name1,
            )
            shutil.copyfile(
                config.DOWNLOAD_FOLDER + "/" + weekly_cron_file_name2,
                config.DOWNLOAD_FOLDER + "/" + daily_cron_file_name2,
            )
            log_info(
                f"files copied from weekly cron to daily cron {daily_cron_file_name1,daily_cron_file_name2}",
                MODULE_CONTEXT,
            )
            # msg = generate_email_notification(users, "weekly cron files copied ")
            # send_email(msg)
        else:
            log_info(
                f"files already there in folder {daily_cron_file_name1,daily_cron_file_name2}",
                MODULE_CONTEXT,
            )
            msg = generate_email_notification(
                users, "files already in directory cannot copy"
            )
            send_email(msg)
        return
    except Exception as e:
        log_exception("Error in fetching the data: {}".format(e), MODULE_CONTEXT, e)
        msg = generate_email_notification(
            users, "could not get the data something went wrong : {}".format(e)
        )
        send_email(msg)
        log_exception(
            "Generated alert email in exception weekly cron job : {}".format(str(e)),
            MODULE_CONTEXT,
            e,
        )
        return


def get_trans_user_data_from_db_daily_day_crn():
    users = config.EMAIL_NOTIFIER
    log_info("fetch data started", MODULE_CONTEXT)
    # filename = uuid.uuid4().hex
    daily_cron_file_name1 = config.DAILY_CRON_FILE_NAME1
    daily_cron_file_name2 = config.DAILY_CRON_FILE_NAME2
    # weekly_cron_file_name1 = config.WEEKLY_CRON_FILE_NAME1
    # weekly_cron_file_name2 = config.WEEKLY_CRON_FILE_NAME2
    # file_save = str(filename)[:-10]+'_USER_WISE_JUD_Org_level_Statistics.csv'
    if os.path.exists(
        config.DOWNLOAD_FOLDER + "/" + daily_cron_file_name1
    ) and os.path.exists(config.DOWNLOAD_FOLDER + "/" + daily_cron_file_name2):
        pass
    else:
        msg = generate_email_notification(
            users, "could not get the data files not found"
        )
        send_email(msg)
        log_info(
            f"Generated alert email for daily cron (files not found),{daily_cron_file_name1,daily_cron_file_name2} ",
            MODULE_CONTEXT,
        )
    user_docs = stats.get_all_users_active_inactive(usr_collection)
    log_info(
        f"Data returned from user {config.USER_COLLECTION} collection", MODULE_CONTEXT
    )
    try:
        df = pd.read_csv(config.DOWNLOAD_FOLDER + "/" + daily_cron_file_name1)
        from_datee = df["created_on"].max()
        from_date = datetime.datetime.strptime(str(from_datee), "%Y-%m-%d %H:%M:%S.%f")
        now = datetime.datetime.now()
        date_time = now.strftime("%Y-%m-%d")
        end_date = datetime.datetime.strptime(str(date_time), "%Y-%m-%d")
        # from_date, end_date = stats.get_time_frame_for_analytics()
        for doc in user_docs:
            # log_info(f'fetching details for {doc} userID',MODULE_CONTEXT)
            ch_docs = stats.fetch_data_for_language_trans_tokenized_for_scheduer_only(
                ch_collection, doc, from_date, end_date
            )
            saved_docs = stats.fetch_data_for_userwise_trans_user_tokenized(
                ch_collection, doc, from_date, end_date
            )
            # log_info(f'Details collected for for userID : {doc} ',MODULE_CONTEXT)
            write_to_csv_user_daily_crn(
                [x for x in ch_docs],
                (config.DOWNLOAD_FOLDER + "/" + daily_cron_file_name1),
            )
            write_to_csv_user_daily_crn(
                [x for x in saved_docs],
                (config.DOWNLOAD_FOLDER + "/" + daily_cron_file_name2),
            )
        log_info(
            f"Data written into files {daily_cron_file_name1,daily_cron_file_name2}",
            MODULE_CONTEXT,
        )
        return
    except Exception as e:
        log_exception("Error in fetching the data: {}".format(e), MODULE_CONTEXT, e)
        msg = generate_email_notification(
            users, "could not get the data something went wrong : {}".format(e)
        )
        send_email(msg)
        log_exception(
            "Generated alert email in exception daily cron job : {}".format(str(e)),
            MODULE_CONTEXT,
            e,
        )
        return
