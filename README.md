# Django Weather Checking App

### Use:
Type the address or drag the map marker to see current weather, 24 hour forecast as well as a 5 day forecast graph  for that location.
Includes actual temp, 'feel' temp, wind speed and direction as well as cloud cover.

Allows user to select similar addresses to the one searched in case of typo/marker-misplace in drop-down.

Searched addresses can be saved and viewed.

###### Considerations:
- Use generic class-based as well as method views
- Use ajax along with standard HTML POST/GET
- Use JS to pass and manage info on FE
- Make multiple API calls per request.  Dynamic API fire sequence based on query info received

###### To do:
- Add Imperial/Metric toggle to set units displayed
- Update line graph aesthetics/readablity
- Manage Django localisation/unlocalisation of timezones (timezones calculated correctly but django templating gives unexpected results sometimes)

