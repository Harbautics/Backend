Our backend framework will involve the usage of Python, with Flask and mySQL to handle the API and database portions. This will be hosted on AWS

# Current File Structure
```bash
├── Applicant.AIBackEnd
│   ├── Cost.h
│   ├── Driver.cpp
│   ├── Load_data.h
│   ├── Network.h
│   ├── databaseAPISkeleton.py
│   └── groupInformationAPI.py
├── README.md
├── base_queries.txt
├── json.txt
└── sql_structure.txt
```

Tentative API Routes:
------------------------------------------------

```
//single organization
OrganizationInformation API
{
	name,
	id,
	members[] {
		id,
		name
	},
	applications[] {
		id,
		name,
		status,
		description,
		users[] {
			id
			name,
		},
		questions[] {
			question
			type, ( can be text entry, dropdown)
			answers[]: (blank if entry, potential answers otherwise)
		}
	}
}

//add to list
joinOrg
//remove from list
leaveOrg
	
//get all orgs for a given user
getAllOrgs (
	OrganizationInformation[]
	
)

//user submission of appid
submitApp 
{
		appid,
		name,
		questions {
			answers[]
		}
}

//all apps for a given user
getAllApps
{
	applications [] {
		appid,
		orgname,
		name,
		description
		status,
		questions[]
			questions,
			answer
	}

}
```	
	


