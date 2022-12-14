# Django Weather Checking App

### Use:
Type the address or drag the map marker to see current weather, 24 hour forecast as well as a 5 day forecast graph  for that location.
Includes actual temp, 'feel' temp, wind speed and direction as well as cloud cover.

Allows user to select similar addresses to the one searched in case of typo/marker-misplace in drop-down.

Searched addresses can be saved and viewed.

###### Considerations:
- Use generic class-based as well as method views
- Use AJAX along with standard HTML POST/GET
- Use JS/jQuery to pass and manage info on FE
- Make multiple API calls per request. Dynamic API fire-sequence based on form used to submit

###### To do:
- Add Imperial/Metric toggle to set units displayed
- General Aesthetics/UI upgrade
- Record sorting/filtering
- Complete CRUD, currently only creating/reading
- Update line graph aesthetics/readablity (Set y-axis locations)
- Manage Django localisation/unlocalisation of timezones (timezones calculated correctly but django templating gives unexpected results sometimes)


