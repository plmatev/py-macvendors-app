# py-macvendors-app
py-macvendors-app is simple yet efficient multi-container Docker application written in Python and using FastAPI and MongoDB as backend to get MAC address vendor information.
It is using IEEE public registry (https://regauth.standards.ieee.org/standards-ra-web/pub/view.html#registries) to download and parse current OUI/MAC Address Blocks - currently set to once per week.\
This project started as a replacement of external API that Golang library we had in our project, was using.

# Installation
* Export shell variables "mongo_user" and "mongo_password"
* Rename .env.example files to .env and change the username and password to match the exported variables
* docker-compose up -d --build

# Usage
### OUI Block details
##### Request
```
curl -X 'GET' \
  'http://localhost:8000/api/v1/oui/dc:2c:6e:77:3d:c6' \
  -H 'accept: application/json'
```

##### Response
```
{
  "result": {
    "company": "Routerboard.com",
    "mac_prefix": "DC:2C:6E",
    "address": "Mikrotikls SIA Riga Riga LV LV1009",
    "start_hex": "DC2C6E000000",
    "end_hex": "DC2C6EFFFFFF",
    "country": null,
    "type": "MA-L"
  }
}
```


### OUI Block Company name
##### Request
```
curl -X 'GET' \
  'http://localhost:8000/api/v1/vendorname/dc:2c:6e:77:3d:c6' \
  -H 'accept: application/json'
```

##### Response
```html
Routerboard.com
```


### All OUI Blocks assigned to Company
##### Request
```
curl -X 'GET' \
  'http://localhost:8000/api/v1/company/cisco' \
  -H 'accept: application/json'
```

##### Response
```
[
  {
    "company": "Cisco Systems, Inc",
    "start_hex": "F4BD9E000000",
    "end_hex": "F4BD9EFFFFFF"
  },
  {
    "company": "Cisco Systems, Inc",
    "start_hex": "084FA9000000",
    "end_hex": "084FA9FFFFFF"
  },
.
.
.
<omitted>
  {
    "company": "Cisco Systems, Inc",
    "start_hex": "E462C4000000",
    "end_hex": "E462C4FFFFFF"
  }
]
```

# License
See the [LICENSE](https://github.com/plmatev/py-macvendors-app/blob/main/LICENSE.md) file for license rights and limitations (MIT).
