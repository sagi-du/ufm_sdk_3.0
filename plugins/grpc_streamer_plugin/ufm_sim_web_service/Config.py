import re
import subprocess
from enum import Enum
import os

class Constants:
    VERSION = '1.0.0'
    CONF_LOGFILE_NAME = 'log_file_name'
    UFM_HTTP_PORT = 443
    UFM_PLUGIN_PORT = 8001
    PLUGIN_HELP = f"This plugin version- {VERSION} is for getting rest apis from the UFM using grpc.\n" \
                  f"The plugin can send the rest api once or stream in intervals, " \
                  f"or even to subscribe to known client and receive all the data sending to that client.\n" \
                  f"To start create a session using CreateSession and add destination, with AddDestination." \
                  f"Then choose RunOnceJob - receive once rest api, RunStreamJob - receive stream of rest api or SubscribeToStream to subscribe to a client results.\n" \
                  f"Please see the proto file in protos for the full API."
    CONF_USERNAME = 'admin'
    CONF_PASSWORD = 'password'
    DEF_LOG_FILE = 'ufm_grpc_streamer.log'
    REST_URL_EVENTS = "/ufmRest/app/events"
    REST_URL_ALARMS = "/ufmRest/app/alarms"
    REST_URL_LINKS = "/ufmRest/app/links"
    REST_URL_JOBS = "/ufmRest/app/jobs"
    REST_DEFAULT_INTERVAL_LOW = 10
    REST_DEFAULT_INTERVAL_HIGH = 60

    UFM_GRPC_STREAMER_CONF_NAME = "ufm_grpc_streamer.conf"
    GRPC_STREAMER_DEF_PATH = "/etc/grpc_streamer"
    GRPC_STREAMER_SERVICE_PATH = "/lib/systemd/system/grpc_streamer.service"

    LOG_SERVER_START = "Starting server with host %s"
    LOG_SERVER_STOP = "Stopping server with host %s"
    LOG_SERVER_HOST = "Config Server with host %s."
    LOG_CONNECT_UFM = "Connecting to UFM server, %s"
    LOG_NO_REST_DESTINATION = "Cannot add new destination without any rest calls. check the RESTCall enum for all the rest api calls"
    LOG_CANNOT_UFM = 'Cannot connect to the ufm server. %s'
    LOG_CANNOT_SESSION = "Wasn't able to create session to the ufm, Connection Error, please see this exception.%s"
    LOG_CANNOT_DESTINATION = "Cannot create destination. %s"
    LOG_CANNOT_NO_SESSION = "Server need a Session to the UFM to do this action, please use CreateSession"
    LOG_CREATE_SESSION = "Creating new session to the ufm. %s"
    LOG_CREATE_DESTINATION = "Creating new destination: %s"
    LOG_EXISTED_DESTINATION = "Already exists destination: %s"
    LOG_NO_EXIST_DESTINATION = "No exists Destination:%s"
    LOG_EDIT_DESTINATION = "Editing an existing destination to new params.%s"
    LOG_DELETE_DESTINATION = "Deleting destination. %s"
    LOG_LIST_DESTINATION = "Get the list of existing destinations."
    LOG_CALL_SERIALIZATION = "Called to do a serialization with all destinations."
    LOG_CALL_STOP_STREAM = "Called to stop the stream of running job. %s"
    LOG_RUN_JOB_ONCE = "Called to extract api data from a job once. %s"
    LOG_RUN_JOB_Periodically = "Called to extract api data from a job periodically. %s"
    LOG_RUN_STREAM = "Called to run stream an api data from a new destination. %s"
    LOG_RUN_ONCE = "Called to run once an api data from a new destination. %s"
    LOG_CALL_SUBSCRIBE = "Called to subscribe to ID and stream data when a stream with that ID is used. %s"
    LOG_GET_PARAMS = "Called to get api params from a job. %s"
    LOG_CREATE_STREAM = "Configurate the stream with job. %s"
    LOG_START_STREAM = "String to stream job with threads. %s"
    LOG_STOP_STREAM = "Stopping stream because client stop connecting to the server. %s"
    ERROR_NO_SESSION = "Cant run client without session, please use CreateSession first. Need to create a session"
    ERROR_NO_CLIENT = "Cant run client without creating Destination, please use AddDestination first."
    ERROR_NO_IP_FOUND = "CLIENT IP NOT FOUND, Cannot continue with the action."

    REST_DEFAULT_INTERVAL = 30
    REST_DEFAULT_DELTA = False


class GENERAL_UTILS:

    @staticmethod
    def run_cmd(command):
        proc = subprocess.Popen(command, shell=True, close_fds=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate()
        stdout = stdout.decode("ascii")
        stderr = stderr.decode("ascii")
        return proc.returncode, str(stdout.strip()), str(stderr.strip())

    @staticmethod
    def getGrpcStreamConfFile():
        cmd = 'cat %s | grep ConditionPathExists' % Constants.GRPC_STREAMER_SERVICE_PATH
        ret, path, _ = GENERAL_UTILS.run_cmd(cmd)
        if ret == 0 and path:
            path = path.split('=')[1]
            return "%s/%s" % (os.path.dirname(path), Constants.UFM_GRPC_STREAMER_CONF_NAME)
        else:
            return "%s/%s" % (Constants.GRPC_STREAMER_DEF_PATH, Constants.UFM_GRPC_STREAMER_CONF_NAME)


class RESTCall(Enum):
    Events = (Constants.REST_URL_EVENTS, Constants.REST_DEFAULT_INTERVAL_LOW, True)
    Alarms = (Constants.REST_URL_ALARMS, Constants.REST_DEFAULT_INTERVAL_LOW, True)
    Links = (Constants.REST_URL_LINKS, Constants.REST_DEFAULT_INTERVAL_HIGH, False)
    Jobs = (Constants.REST_URL_JOBS, Constants.REST_DEFAULT_INTERVAL_HIGH, False)

    def __init__(self, extension, interval=10, delta=False):
        self.location = extension
        self.interval = interval
        self.delta = delta

    @classmethod
    def __contains__(cls, value):
        return value in cls._member_names_

