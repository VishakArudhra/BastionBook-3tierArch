# BastionBook-3tierArch

* The frontend and backend code files will be in the **main** branch which you're already in.

* For the ansible playbook files switch to the **deploy** branch.

**A temporary note about the deploy branch**

Since the commit pushed to attempt the containerized deployment of our application in the **main** branch, file structure has been changed significantly to affect the successful working of this branch.

Therefore, until this incosistency is fixed, those with limited knowledge might not find it easy to work with the **deploy** branch and execute the *ansible playbooks* . 

### Setting Up Custom Domain Address for your API Gateway

It can be be a cumbersome job to keep rebuilding the image with a different API gateway endpoint each time some error occurs related to it. Therefore, it's best to keep a single custom domain address to route all API requests from the application.

#### A description of caution before creating hosted zones for your custom domain API Gateway Endpoint

Let's suppose `example.com` is the domain we've bought and let's assume request routed via this domain may go to different cloud resources in different AWS accounts.

In this case, `Route53` hosted zones created across these accounts must be created in different 'subdomain names'.

e.g.,
```
1XXXXXX70XX2 - api.example.com
2XXX90707XXX - api1.example.com
```

Creating all the hosted zones with the same domain name for e.g., `example.com` might disrupt DNS request routing through to any specific AWS resource hosted at a specific subdomain.

In this case, no matter how unique are the A records across the different hosted zones, there won't be consistent success in the domain resolution.

For setting up custom domain endpoint for the API Gateway, [this](https://wenheqi.medium.com/route-api-gateway-api-to-a-custom-domain-name-using-route53-251bc7f6fe75) was the referred article which contains all the relevant steps in detail to setup a custom domain API gateway endpoint.

### Containerization of the previously VM-hosted 3-tier Architecture based App

The previous 'VM-hosted' application setup isn't much different from the currently containerized setup:

1) The application would be served through multiple *gunicorn* processes waiting for requests in a .sock file.
2) An nginx process would be listening at port 80 distributing traffic requests to the gunicorn processes through the .sock file, thereby accomplishing the 'load-balancing'.
3) All these tools though would run as services or daemons.

Let's take a look at the file structure starting from the .yaml file used to initiate containers through docker-compose:

```
.
├── README.md
├── bastionbook-backend
│   └── lambda-backend.py
├── bastionbook-frontend
│   ├── Dockerfile
│   ├── bastionbook.py
│   ├── node_modules
│   ├── requirements.txt
│   ├── static/
│   ├── templates/
│   ├── wsgi.py
│   └── yarn.lock
├── compose.yaml
└── nginx-load-balancers
    ├── Dockerfile
    └── default.conf
```

Initiate the containers by running the following command in the same directory where `compose.yaml` file lies:

`docker-compose up --build -d --scale frontend=2`

This would both build the images and instantiate containers off of them and place all the containers it's created in the same network for communication amongst them.

#### how container-to-container communication works:

1) While frontend containers would be listening on their ports `5000`, the nginx container would be listening on its port `80` that is supposed to be mapped to the same port of the host.

2) This way, the same way requests would have been forwarded in the earlier setup, they would be forwarded by the nginx container to the frontend containers by resolution of the respective DNS Aliases of the latter.

3) The [DNS Aliases](https://docs.docker.com/get-started/07_multi_container/#start-mysql) is how an nginx container can communicated to their target application containers.

#### Reference we've used to write our *frontend* and *nginx* docker files:

https://www.geeksforgeeks.org/load-balancing-flask-application-using-nginx-and-docker/

https://github.com/docker/awesome-compose/blob/master/nginx-wsgi-flask/README.md
