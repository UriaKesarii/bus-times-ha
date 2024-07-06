# bus-times-ha
***Integration of Real-time Israel Bus Data Retrieval with Home Assistant Assist***


In this README it will be described how with a few steps, we can ask Assist in Home Assistant to get information on how long it will take for bus lines at a specific station to arrive.

Attached are a few images for example.



<kbd><img src="https://github.com/UriaKesarii/bus-times-ha/blob/main/images/markup_1000069993.jpg" width="300"></kbd>       <kbd><img src="https://github.com/UriaKesarii/bus-times-ha/blob/main/images/markup_1000069984.jpg" width="300"></kbd>



As you can see from the images above, you can get information about bus lines by:
1. `A reserved keyword`: "לעבודה" or "לבית".
2. `Providing the station number and the lines`: *'תחנה=XXX קווים=nn,nn'* or *'ת=XXX ק=nn,nn'* or *'תחנה XXX קווים nn,nn'* or *'ת XXX ק nn,nn'*
3. `Providing only the station number`: If you only provide the station number, you will receive information about all the lines at the station you provided.



## Add A Python Script

1. Create a new folder named `python_scripts` under the config `directory`.
2. Create a new file named `get_bus_times.py`.
3. Copy the code that appears [here](https://github.com/UriaKesarii/bus-times-ha/blob/main/get_bus_times.py) into the new file you created.


## Use The Shell Command Integration

Using the [Shell Command integration](https://www.home-assistant.io/integrations/shell_command/), we can run the script we just created. Add the following lines to the `configuration.yaml` file:

```
shell_command:
  get_bus_time: "/bin/bash -c '/config/python_scripts/get_bus_times.py {{ station }} {{ lines }}'"
```

After adding the script and Shell Command integration, we will restart Home Assistant.

## A Quick Check.

A quick check to see that everything is working as expected:



1. Navigate to [![Open your Home Assistant instance and show your service developer tools with a specific service selected.](https://my.home-assistant.io/badges/developer_call_service.svg)](https://my.home-assistant.io/redirect/developer_call_service/?service=shell_command.get_bus_time)
2. Click on `call service` If the response looks like this
```
stdout: "Usage: ./get_bus_times.py <station_number> <bus_lines>"
stderr: ""
returncode: 1
```
 it's working correctly. if not, something might have been missed.



