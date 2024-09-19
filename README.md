
# Setting Up the Project Locally





## Run Locally

Clone the Repository:
```cmd
  git clone https://github.com/Jawad652923/Travel_CRM.git
```

Go to the project directory

```cmd
  cd Travel_CRM
```

Create and Activate a Virtual Environment:

```cmd
python -m venv venv
venv\Scripts\activate
```
Install Dependencies:
```cmd
pip install -r requirements.txt
```


### Database Config:

NOTE: Configure the Database Update the DATABASES setting in settings.py . comment out the postgresql database settings and uncomment the default database settings


Run Migrations:
```cmd
python manage.py makemigrations

python manage.py migrate

```

Create Super_User:

```cmd
python manage.py createsuperuser
```

Run Server:

```cmd
python manage.py runserver
```



The API will be accessible at http://127.0.0.1:8000/.


## Description On Roles & Permission:

- Admin can access all resources, update , delete and post anything he wants.
- While the sales agenet have some restriction, he can only view and manage those customer which he assigned to.
- He can't be able to delete any customer data.
- He can view and manage Inquiries,Proposals and services related to their customers.



## API Endpoints:

#### For Authentication:

```http
  POST /api/auth/token/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `username` | `string` | **Required**. The username of the user. |
| `password` | `string` | **Required**. The password of the user. |

```http
  POST /api/auth/token/refresh/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `refresh` | `string` | **Required**. The refresh_token to get the access token. |

```http
  POST /api/auth/token/verify/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `token` | `string` | **Required**. Pass access to verify. |


#### GET Customer list
 
```http
  GET /api/customers/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `access`  | `string` | **Required**. The access_token to get the list. |


#### GET Specific Customer 

```http
  GET /api/customers/${id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `access`  | `string` | **Required**. The access_token to check authenticity. |

#### POST Customer

```http
  POST /api/customers/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `access`  | `string` | **Required**. The access_token to check authenticity. |
| `name`  | `string` | **Required**. The name of the customer. |
| `email`  | `string` | **Required**. The email of the customer. |
| `phone_no`  | `string` | **Required**. The phone_no of the customer. |
| `address`  | `string` | **Required**. The address of the customer. |


#### Update Specific Customer 

```http
  PUT /api/customers/${id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `access`  | `string` | **Required**. The access_token to check authenticity. |
| `id` | `string` | **Required**. A Customer_id should pass in URL. |
| `field_name` | `string` | **Required**. A field_name that you wants to Update. |

#### Delete Specific Customer 
    NOT ONLY ADMIN CAN DELETE ANY CUSTOMER
```http
  DELETE /api/customers/${id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `access`  | `string` | **Required**. The access_token to check authenticity. |
| `id` | `string` | **Required**. A Customer_id should pass in URL. |


#### GET Inquiry list
 
```http
  GET /api/inquiries/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `access`  | `string` | **Required**. The access_token to check authenticity. |


#### GET Specific Inquiry 

```http
  GET /api/inquiries/${id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `access`  | `string` | **Required**. The access_token to check authenticity. |
| `id` | `string` | **Required**. A Inqury_id should pass in URL. |


#### POST Inquiry

```http
  POST /api/inquiries/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `access`  | `string` | **Required**. The access_token to check authenticity. |
| `details`  | `string` | **Required**. The details of an inquiry. |
| `status`  | `string` | **Required**. The status of an inquiry. |
| `customer`  | `string` | **Required**. The Customer_id which is related to  an inquiry. |
| `services`  | `string` | **Required**. The service_id which is related to an inquiry. |


#### Update Specific Inquiry 

```http
  PUT /api/inquiries/${id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `access`  | `string` | **Required**. The access_token to check authenticity. |
| `id` | `string` | **Required**. A Inquiry_id should pass in URL. |
| `field_name` | `string` | **Required**. A field_name that you wants to Update. |

#### Delete Specific Inquiry 
```http
  DELETE /api/inquiries/${id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `access`  | `string` | **Required**. The access_token to get the Customer. |
| `id` | `string` | **Required**. A Inquiry_id should pass in URL. |



#### GET Service list
 
```http
  GET /api/services/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `access`  | `string` | **Required**. The access_token to check authenticity. |


#### GET Specific Service 

```http
  GET /api/services/${id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `access`  | `string` | **Required**. The access_token to check authenticity. |
| `id` | `string` | **Required**. A service_id should pass in URL. |


#### POST Service

```http
  POST /api/services/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `access`  | `string` | **Required**. The access_token to check authenticity. |
| `name`  | `string` | **Required**. The name of the Service. |
| `description`  | `string` | **Required**. The Description of Service. |
| `price`  | `string` | **Required**. The Price of Service. |


#### Update Specific Service 

```http
  PUT /api/services/${id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `access`  | `string` | **Required**. The access_token to check authenticity. |
| `id` | `string` | **Required**. A Service_id should pass in URL. |
| `field_name` | `string` | **Required**. A field_name that you wants to Update. |

#### Delete Specific Service 
```http
  DELETE /api/services/${id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `access`  | `string` | **Required**. The access_token to check authenticity. |
| `id` | `string` | **Required**. A Service_id should pass in URL. |




#### GET Proposal list
 
```http
  GET /api/proposals/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `access`  | `string` | **Required**. The access_token to check authenticity. |


#### GET Specific Proposal 

```http
  GET /api/proposals/${id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `access`  | `string` | **Required**. The access_token to check authenticity. |
| `id` | `string` | **Required**. A proposal_id should pass in URL. |


#### POST Proposal

```http
  POST /api/proposals/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `access`  | `string` | **Required**. The access_token to check authenticity. |
| `inquiry`  | `string` | **Required**. The Inquiry_id related to the proposal. |
| `details`  | `string` | **Required**. The details of proposal. |
| `services`  | `string` | **Required**. The service_id related to proposal. |
| `status`  | `string` | **Required**. The status of proposal. |
| `cost`  | `string` | **Required**. The cost of proposal. |


#### Update Specific Proposal 

```http
  PUT /api/proposals/${id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `access`  | `string` | **Required**. The access_token to check authenticity. |
| `id` | `string` | **Required**. A proposal_id should pass in URL. |
| `field_name` | `string` | **Required**. A field_name that you wants to Update. |

#### Delete Specific Proposal 
```http
  DELETE /api/proposals/${id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `access`  | `string` | **Required**. The access_token to check authenticity. |
| `id` | `string` | **Required**. A proposal_id should pass in URL. |





