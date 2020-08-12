#!/usr/bin/env python
# coding: utf-8



import meraki
import pandas as pd
import os
import csv


# Defining your API key as a variable in source code is not recommended
#API_KEY = 'INSERT YOUR API KEY HERE'
# Instead, use an environment variable as shown under the Usage section
# @ https://github.com/meraki/dashboard-api-python/

dashboard = meraki.DashboardAPI()

#Open the csv containing the MS switches serial numbers
#Using utf-8-sig because by default it adds weird characters on the first row imported

f = open('last.csv', encoding="utf-8-sig")
csv_f = csv.reader(f)
for row in csv_f:
        serial =row


        response = dashboard.switch.getDeviceSwitchPortsStatuses(
        serial[0]
        )

        #Place response into a dataframe
        switch_port_df = pd.DataFrame(response)

        #Limit dataframe to required columns
        switch_port_df = switch_port_df[['portId','status']]


        # retrieve llpd server name for port 1 an place into "name" variable
        #This is because we are retrieving the lldp of the device connected on the uplink port to rename the output csv rather than using serial number
        #So if your uplink port is different please modify accordingly 

        df = pd.DataFrame(response)

        #To avoid confusion with portID we are renaming it portID_orig
        df.rename(columns={'portId':'portId_orig'}, inplace=True)
        df_2 = pd.concat([df.portId_orig , (df['lldp'].apply(pd.Series))], axis = 1)
        name = df_2.loc[df_2.portId_orig=='1'].systemName.item()

        #Save switch_port_df as a CSV using the lldp name variable
        switch_port_df.to_csv(str(name) + '.csv', index = False )

