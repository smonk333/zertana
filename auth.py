import requests

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

#making post requests with the provided usernames and passwords
rATL = requests.post(atlBase+apiUrlBase+'/v1/session/add', auth=(pvdcAdd+usernATLAS, passwATLAS))
rLAS = requests.post(lasBase+apiUrlBase+'/v1/session/add', auth=(pvdcAdd+usernATLAS, passwATLAS))
rSPA = requests.post(spaBase+apiUrlBase+'/v1/session/add', auth=(netAdd+usernSPA, passwSPA))

#setting a variable equal to each site's bearer token, returned from the post request
sessionTokenATL = rATL.headers['x-zerto-session']
sessionTokenLAS = rLAS.headers['x-zerto-session']
sessionTokenSPA = rSPA.headers['x-zerto-session']

#making files for the bearer tokens to go in
fileATL = open("tokenATL.txt", "w")
fileLAS = open("tokenLAS.txt", "w")
fileSPA = open("tokenSPA.txt", "w")

#yeeting ATL session token into a file
fileATL.write(sessionTokenATL)
fileATL.close()

#yeeting LAS session token into a file
fileLAS.write(sessionTokenLAS)
fileLAS.close()

#yeeting SPA session token into a file
fileSPA.write(sessionTokenSPA)
fileSPA.close()