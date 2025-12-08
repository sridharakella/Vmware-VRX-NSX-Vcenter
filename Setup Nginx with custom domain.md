# Steps to setup Nginx & SSL on AWS EC2

- **Prerequisite**  
You should have an application running on EC2 inctance on    
`http://<your-ec2-public-ip>:5000`  
 you can paste below script in userData while launcing EC2 instance to setup node js application quickly   
  ```
  #!/bin/bash
  # Update packages
  yum update -y

  # Install git
  yum install -y git

  # Install Node.js v20 from NodeSource
  curl -fsSL https://rpm.nodesource.com/setup_20.x | bash -
  yum install -y nodejs
  
  # Install pm2 globally
  npm install -g pm2
  
  # Go to EC2 default user’s home directory
  cd /home/ec2-user  
  
  # Clone your repo
  git clone https://github.com/mukeshphulwani66/hello-world-node.git  
  
  # Change to repo directory
  cd hello-world-node
  
  # Install dependencies
  npm install
 
  # Start the app with PM2
  pm2 start index.js

  ```

- **Set up Nginx on your EC2 as a reverse proxy**    
  A reverse proxy sits in front of your backend app (like Node.js) and forwards incoming requests to it.  
  ```
  sudo yum install nginx -y  
  sudo systemctl start nginx
  sudo systemctl enable nginx
  ```       
  Edit default config  
  ```
  sudo vim /etc/nginx/nginx.conf
  ```  
  Add this inside the http {} block:
  ```
  server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://localhost:5000;
     }
   }
  ```
  Reload Nginx:  
  ```
  sudo systemctl restart nginx
  ```  
  You should be now able to access the application on `http://<your-ec2-public-ip>`  
  
- **SSL certificate set up using Let’s Encrypt on your EC2 instance with Nginx**  
  We’ll use Certbot, the easiest way to generate and install SSL certificates.  
  
  Step 1: Install Certbot and Nginx plugin  
  ```
  sudo yum install -y certbot python3-certbot-nginx
  ```
  Step 2: Request a certificate
  Replace yourdomain.com with your real domain:  
  ```
  sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
  ```  
  Certbot will:
  Ask for your email
  Agree to terms
  Automatically update your Nginx config
  Reload Nginx with the SSL cert
    
  Step 3: 🚀 Done!
  Now your site should be accessible via: `https://yourdomain.com`  
    
    
  
  
 