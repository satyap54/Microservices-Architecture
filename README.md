# Microservices Architecture

![](https://github.com/satyap54/Microservices-Architecture/blob/main/Microservices/Microservices-Architecture.drawio)

#### Admin service
Contains end-points to manage accounts and post data on the platform. The end-points enable admin to manage all the user-accounts as well as post data to other services. Users can use some of the end-points for authentication.

Method	| Path	| Description	| Authenticated	User | Admin Only | Allow Any
------------- | ------------------------- | ------------- |:-------------:|:----------------:|:----------------:|
POST	| api/accounts/signup	| Create a new account	|  | | x
POST	| api/accounts/login	| Get your JWT for authentication	|  | | x
GET	| api/accounts/me	| Get authenticated user's email-id and pk	|  x  | 	 | 
GET	| api/events/	| List of events posted by admin	|  |  |
POST	| api/events/	| Post about a new event	|  | x |
GET	| api/events/{pk}	| Get details of a particular event	|  x |  |
PUT	| api/events/{pk}	| Update a particular event	|  | x |
DELETE	| api/events/{pk}	| Delete a particular event	|   | x |

#### Event service
Stores information about the attendees of an event.

Method	| Path	| Description	| Authenticated	User | Admin Only | Allow Any
------------- | ------------------------- | ------------- |:-------------:|:----------------:|:----------------:|
GET	| /api/events/	| Lists active events	| x | | 
POST| /api/events/{event_id}/attend	| Let the admin know that you'll attend the event with this id	| x | | 
