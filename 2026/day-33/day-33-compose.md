# Day 33 – Docker Compose: Multi-Container Basics
## Task 1: Install & Verify
+ Check if Docker Compose is available on your machine
   + docker-compose
+ Verify the version
   + docker compose version
    ```
    +  Docker Compose version v5.0.2
     ```
<img width="980" height="123" alt="Screenshot (237)" src="https://github.com/user-attachments/assets/04715529-37e1-4661-bef5-8c54e0235345" />
<img width="1033" height="205" alt="Screenshot (236)" src="https://github.com/user-attachments/assets/60801a1b-a290-490a-a68c-f9d4d0ea9948" />


------------------------------------------------------------------------------------------------------------------------------------------------------------------


     
## Task 2: Your First Compose File
+ Create a folder compose-basics
   + ```mkdir compose-basics ```
   + ```cd compose-basics```
   + ```vim docker-compose.yml```
+ Write a docker-compose.yml that runs a single Nginx container with port mapping
  ```
  services:
      web:
        image: nginx
        container_name: mynginx
        port :
         - "8080:80"
  ```
+ Start it with docker compose up
    + ```docker compose up ```
+ Access it in your browser

  <img width="1920" height="337" alt="Screenshot (224)" src="https://github.com/user-attachments/assets/ca1238b2-4678-47fa-b845-42f0c505771f" />

+ Stop it with docker compose down
    + ``` docker compose down ```


----------------------------------------------------------------------------------------------------------------------------------------------------------------------

## Task 3: Two-Container Setup
+ Write a docker-compose.yml that runs:
+ A WordPress container
+ A MySQL container
+ They should:

+ Be on the same network (Compose does this automatically)
+ MySQL should have a named volume for data persistence
+ WordPress should connect to MySQL using the service name
```
version: "3.8"

services:
  db:                                    #  A MySQL container
    image: mysql:5.7
    container_name: my-mysql
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: rootpassword
      MYSQL_DATABASE: wordpress
      MYSQL_USER: firdous
      MYSQL_PASSWORD: 12345
    volumes:
      - myvol:/var/lib/mysql               # MySQL should have a named volume for data persistence
  wordpress:                               # A WordPress container
    image: wordpress:latest
    container_name: my-wordpress
    restart: always
    ports:
      - "8080:80"
    environment:
      WORDPRESS_DB_HOST: db:3306
      WORDPRESS_DB_USER: firdous
      WORDPRESS_DB_PASSWORD: 12345
      WORDPRESS_DB_NAME: wordpress
    depends_on:
      - db                                #  WordPress should connect to MySQL using the service name

volumes:
  myvol:
```
+ Start it, access WordPress in your browser, and set it up.
<img width="1920" height="709" alt="Screenshot (228)" src="https://github.com/user-attachments/assets/c0aad27f-0fea-478e-a445-2d7af96a7ab4" />

  
+ Verify: Stop and restart with docker compose down and docker compose up — is your WordPress data still there?
+ yes the data is still there



<img width="1920" height="886" alt="Screenshot (230)" src="https://github.com/user-attachments/assets/499fbdb1-7e6f-453c-ac25-7dface562693" />

------------------------------------------------------------------------------------------------------------------------------------------------------------  

## Task 4: Compose Commands
### Practice and document these:

+ Start services in detached mode
    + ```docker compose up -d```

+ View running services
    + ```docker compose ps```
  
+ View logs of all services
    + ```docker compose logs```
  
+ View logs of a specific service
    + ```docker compose logs wordpress```
  
+ Stop services without removing
   + ```docker compose stop```
  
+ Remove everything (containers, networks)
   + ```docker compose down```
  
+ Rebuild images if you make a change
   + ```docker compose up -d --build```

  --------------------------------------------------------------------------------------------------------------------------------------------------------------

  ## ask 5: Environment Variables
+ Add environment variables directly in your docker-compose.yml
```
MYSQL_ROOT_PASSWORD=firdous
MYSQL_DATABASE=wordpress
MYSQL_USER=wpaliya
MYSQL_PASSWORD=firdous
```
+ Create a .env file and reference variables from it in your compose file
```
  services:
  db:
    image: mysql:5.7
    environment:
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
      MYSQL_DATABASE: ${MYSQL_DATABASE}
      MYSQL_USER: ${MYSQL_USER}
      MYSQL_PASSWORD: ${MYSQL_PASSWORD}
  ```
+ Verify the variables are being picked up
   + ```docker compose config```
<img width="1584" height="343" alt="Screenshot (235)" src="https://github.com/user-attachments/assets/4edbb045-a174-458e-819d-256424fd78f0" />

<img width="1920" height="771" alt="Screenshot (234)" src="https://github.com/user-attachments/assets/70be314c-3bf2-4392-b721-1657a55123e9" />


----------------------------------------------------------------------------------------------------------------------------------------------------------------
  
