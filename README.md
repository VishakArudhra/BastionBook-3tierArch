# BastionBook-3tierArch

* The frontend and backend code files will be in the **main** branch which you're already in.

* For the ansible playbook files switch to the **deploy** branch.

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

For setting up custom domain endpoint for the API Gateway, [this](https://wenheqi.medium.com/route-api-gateway-api-to-a-custom-domain-name-using-route53-251bc7f6fe75) was the referred article.
