# gcp_api_checker
Coding Challenge for Aginic Full Stack Developer Role

#### Assumptions
1. The HTTP call done on the URL for checking is done using a GET request
1. Job retries are done after a short delay, (configured to 2 seconds) before moving on to the next job
1. Neither Frontend UI nor Backend API requires any authentication of the user
    - The Frontend is statically hosted in Google Cloud Storage, and is configured to allow viewing to anyone who has the link for easy use. (This policy can be changed just as easily for deployment)
1. Once the job is completed, (regardless of status code), it is not checked again. Job runner only looks for the newly entered jobs


#### Solution Architecture
1. Frontend
    - Created using Vue.js
    - Automatic refresh of data every 10 seconds
    - Single Page Application for submitting URL and viewing status
    - Hosted on Google Cloud storage [here](https://storage.googleapis.com/checker-static-hosting/index.html).

1. API Server
    - Implemented using Django + Django Rest Framework
    - Basic CRUD functionality of jobs
    - Hosted using Google App Engine (PaaS)
    - Tests conducted using Postman application for the various API calls
    - Browsable API can be viewed publicly [here](https://shreyas-api-checker.ts.r.appspot.com/api/)
    
1. Data Persistence Layer
    - Provided using Google Cloud SQL, a managed database service
    - Access restricted behind the VPC Firewall provided by Google Cloud Platform
    - All App Engine applications are authorised to connect to the SQL Instance
    - Google Cloud Functions requires a VPC Connection in order to connect to the service (it provides a private IP address for the function to call to the private IP of the SQL Instance)
    - Tests conducted by using local connection proxy provided by Google Cloud
    - Not accessible publicly, so no url
    
1. Job Runner
    - Achieved using Google Cloud Functions (FaaS) as a serverless, stateless runtime environment
    - The deployed function 'Subscribes' to a topic - 'do-job' in order to make the invocation
    - Google Cloud Scheduler is used to 'Publish' a message to the same topic every 30 seconds to perform the jobs
        - CRON Scheduler only allows invocations every minute, so two invocations are done
            1. First, that has no delay, so the function checks for data directly
            1. Seconds, has a 30 second delay, so the function waits for 30 seconds, then checks for new jobs
    - Function processing connects to the Database and 'Locks' the row for updating as it is possible that other instances are accessing the same database
        - If a function wants access to the same row, then it waits until the first function has committed its result
        - If the function just wants any other row, then the database will allow access to that instance and maintain separate locks for each row
        - Django backend, also reads the database only in its committed state
        - This way, multiple processes accessing the same database can be achieved without any synchronization issues
    - GCP Functions are horizontally scalable, so an admin can change the maximum number of allowed instances in Cloud Console in order to account for extra load
        - Moreover, the function backend can scale the instances down when they are not in use, so that resources as well as money is not wasted when there is no load
   
#### Design Decisions
1. Google Cloud Platform (for it's free tier)
    - The latest update to the free tier of GCP provides 3 Months of free access to all services
    - It has a US$300 Limit to it, but it is enough for this project
    - Although AWS provides 1 year of free tier service, it limits the user with certain instances and lower powered servers
    - Heroku free tier doesn't allow hosting in Australia region
    - MS Azure free tier services are limited to 30 days, it is too little for comfort specially when 3 month is available
    
1.  Google App Engine (for backend)
    - Managed service for API Hosting
    - Auto scaling (both horizontal and vertical) possible, and performed by the Cloud backend depending on load
    - Cloud managed certificates for HTTPS
    - Good documentation and minimal configuration
    - Easy to migrate to other services (if required) as it is a Django Application at the base
    
1. Google Cloud Functions (for job runner)
    - First thought that usually occurs to many would be setting up a bunch of identical VMs behind a load balancer and call it a day. However, cloud technologies have evolved to an extent where they are capable of managing automatic horizontal scaling according to need
    - This can be said for App Engine as well, and it was another candidate considered for this task as it supports CRON scheduling
    - But, in the end, the job runner task is a straightforward invocation of a URL and storing its result in the database
    - So, to minimize the implementation, Cloud Functions was chosen
    - These functions are completely internal and can not be accessed from the public internet
    
    
#### Future Scope

1. Implementing other HTTP Requests like POST, PUT, PATCH, DELETE, etc. would be a good feature as some API endpoints require that kind of access
    - Can be done by taking the request type as a dropdown input during job creation and storing it with the job URL
    - Some requests might need additional data that is sent within the request, like POST or PATCH, so another data field will be needed to store it

1. Implementing Authentication and Token based identification
    - For having the ability to distribute and monitor the use of the API by others
    
1. Frontend UI able to re-request the same URL for checking again
    - Either, the backend can clear the same Job's result
    - OR, it can copy the Job URL to a new Job
    