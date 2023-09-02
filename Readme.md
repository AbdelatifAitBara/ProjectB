[![Build using these technologies](https://img.shields.io/badge/Build%20using%20these%20technologies-brightgreen)](https://github.com/AbdelatifAitBara/ProjectB)

[![Vagrant](https://img.shields.io/badge/Vagrant-orange)](https://www.vagrantup.com/)
[![VirtualBox](https://img.shields.io/badge/VirtualBox-blueviolet)](https://www.virtualbox.org/)
[![Python](https://img.shields.io/badge/Python-blue)](https://www.python.org/)
[![Nginx](https://img.shields.io/badge/Nginx-brightgreen)](https://nginx.org/)
[![WordPress](https://img.shields.io/badge/WordPress-informational)](https://wordpress.org/)
[![WooCommerce](https://img.shields.io/badge/WooCommerce-success)](https://woocommerce.com/)
[![REST API](https://img.shields.io/badge/REST%20API-lightgrey)](https://en.wikipedia.org/wiki/Representational_state_transfer)



[![Microservices Stable V1.5](https://img.shields.io/badge/Microservices-Stable%20V1.5-blueviolet)](https://github.com/AbdelatifAitBara/ProjectB)


```
VMs IPs:

- Production Machine       : 192.168.10.10
- CI/CD Server "Jenkins"   : 192.168.10.20

```

```
Containers IPs:

- WooCommerce                            : 192.168.10.10:8888

- Product Microservice                   : 192.168.10.10:8080

- Order Microservice                     : 192.168.10.10:9090

- Jenkins Master                         : 192.168.10.20:5555

```


```
API END POINTS: 

Product Microservice: 


    Generate Token  :  http://192.168.10.10/token_product
    Add Product     :  http://192.168.10.10/add_product
    Update Product  :  http://192.168.10.10/get_product/<id>
    Delete Product  :  http://192.168.10.10:8080/delete_product/<id>
    Get Product     :  http://192.168.10.10/get_product/<id>

Order Microservice: 

    Generate Token  :  http://192.168.10.10/token_order
    Add Order       :  http://192.168.10.10/add_order
    Update Order ²  :  http://192.168.10.10/update_order/<id>
    Delete Order    :  http://192.168.10.10/delete_order/<id>
    Get Order       :  http://192.168.10.10/get_product/<id>

```

- Test AAB branch Lotfi 🤍
- Product Works 100% With TOKEN Protection.
- Order Works 100% With TOKEN Protection.
- Token Valid only for 2 minutes Works 100%
- Reverse Proxy Works 100%.


[![Made with Love](https://img.shields.io/badge/Made%20with-Love-red)](https://github.com/AbdelatifAitBara/ProjectB)