from prometheus_client import start_http_server, Gauge, Enum, Metric, REGISTRY
import requests
import json
import sys
import os
import time


#variables for the API URL base because i'm lazy
apiUrlBase = "palmettovdc.com:9669"
lasBase = "https://laspvdcbrs."
atlBase = "https://atlondbrs."
spaBase = "https://spapvdcbrs."
netAdd = "net3\\"
pvdcAdd = "pvdc\\"


#grab ATL/LAS/SPA bearer tokens and yeet them into a file for prometheus to read from
usernATLAS = input("\nEnter ATL/LAS username (pvdc\\ is added automatically): ")
passwATLAS = input("\nEnter ATL/LAS password: ")

usernSPA = usernATLAS #because they're the same, duh
passwSPA = input("\nEnter SPA password: ")

#i may be stupid, just ignore these for a sec

#making files for the bearer tokens to go in
#fileATL = open("tokenATL.txt", "w")
#fileLAS = open("tokenLAS.txt", "w")
#fileSPA = open("tokenSPA.txt", "w")

#yeeting ATL session token into a file
#fileATL.write(sessionTokenATL)
#fileATL.close()

#yeeting LAS session token into a file
#fileLAS.write(sessionTokenLAS)
#fileLAS.close()

#yeeting SPA session token into a file
#fileSPA.write(sessionTokenSPA)
#fileSPA.close()

class AppMetrics:

    def __init__(self, app_port=1234, polling_interval_seconds=300):
        self.app_port = app_port
        self.polling_interval_seconds = polling_interval_seconds

        #metrics to collect (ATL)
        self.description_ATL = Gauge("descriptionATL", "Alert description (ATL)")
        self.time_ATL = Gauge("timeATL", "What time the alert was generated (ATL)")
        self.affected_vpg_ATL = Gauge("affected_vpgATL", "Which VPG is impacted (ATL)")
        self.site_name_ATL = Gauge("site_nameATL", "Which site is impacted (ATL)")

        #metrics to collect (LAS)
        self.description_LAS = Gauge("descriptionLAS", "Alert description (LAS)")
        self.time_LAS = Gauge("timeLAS", "What time the alert was generated (LAS)")
        self.affected_vpg_LAS = Gauge("affected_vpgLAS", "Which VPG is impacted (LAS)")
        self.site_name_LAS = Gauge("site_nameLAS", "Which site is impacted (LAS)")

        #metrics to collect (SPA)
        self.description_SPA = Gauge("descriptionSPA", "Alert description (SPA)")
        self.time_SPA = Gauge("timeSPA", "What time the alert was generated (SPA)")
        self.affected_vpg_SPA = Gauge("affected_vpgSPA", "Which VPG is impacted (SPA)")
        self.site_name_SPA = Gauge("site_nameSPA", "Which site is impacted (SPA)")

    def run_metrics_loop(self):

        while True:
            self.fetch()
            time.sleep(self.polling_interval_seconds)

    def fetch(self):
        #time to yoink some data, babey !!!!

        #making post requests with the provided usernames and passwords
        rATL = requests.post(atlBase+apiUrlBase+'/v1/session/add', auth=(pvdcAdd+usernATLAS, passwATLAS))
        rLAS = requests.post(lasBase+apiUrlBase+'/v1/session/add', auth=(pvdcAdd+usernATLAS, passwATLAS))
        rSPA = requests.post(spaBase+apiUrlBase+'/v1/session/add', auth=(netAdd+usernSPA, passwSPA))

        #setting a variable equal to each site's bearer token, returned from the post request
        sessionTokenATL = rATL.headers['x-zerto-session']
        sessionTokenLAS = rLAS.headers['x-zerto-session']
        sessionTokenSPA = rSPA.headers['x-zerto-session']

        #grab ATL alerts json
        metricsATL = requests.get(atlBase+apiUrlBase+'/v1/alerts', headers = {"x-zerto-session": sessionTokenATL}).json()

        #grab LAS alerts json
        metricsLAS = requests.get(lasBase+apiUrlBase+'/v1/alerts', headers = {"x-zerto-session": sessionTokenLAS}).json()

        #grab SPA alerts json
        metricsSPA = requests.get(spaBase+apiUrlBase+'/v1/alerts', headers = {"x-zerto-session": sessionTokenSPA}).json()

        #update ATL metrics using the .jsons we just pulled
        self.description_ATL.set(metricsATL["Description"])
        self.time_ATL.set(metricsATL["TurnedOn"])
        self.affected_vpg_ATL.set(metricsATL["AffectedVpgs"])
        self.site_name_ATL.set(metricsATL["Site"])

        #update LAS metrics using the .jsons we just pulled
        self.description_LAS.set(metricsLAS["Description"])
        self.time_LAS.set(metricsLAS["TurnedOn"])
        self.affected_vpg_LAS.set(metricsLAS["AffectedVpgs"])
        self.site_name_LAS.set(metricsLAS["Site"])

        #update SPA metrics using the .jsons we just pulled
        self.description_SPA.set(metricsSPA["Description"])
        self.time_SPA.set(metricsSPA["TurnedOn"])
        self.affected_vpg_SPA.set(metricsSPA["AffectedVpgs"])
        self.site_name_SPA.set(metricsSPA["Site"])

def main():

    polling_interval_seconds = int(os.getenv("POLLING_INTERVAL_SECONDS", "5"))
    app_port = int(os.getenv("APP_PORT", "80"))
    exporter_port = int(os.getenv("EXPORTER_PORT", "9877"))

    app_metrics = AppMetrics(
        app_port=app_port,
        polling_interval_seconds=polling_interval_seconds
    )
    start_http_server(exporter_port)
    app_metrics.run_metrics_loop()

if __name__ == "__main__":
    main()