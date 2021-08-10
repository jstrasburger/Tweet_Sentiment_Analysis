***********************************************
# **Twitter Sentiment Analysis**

### Table of Contents

# Table of Contents
1. ### [Summary](#summary)
2. ### [AWS Utilized](#aws-utilized)
3. ### [Machine Learning Techniques](#machine-learning-techniques)
4. ### [License](#mit-license)

### **Summary**
A Dash Application written and deployed during a course in Applied Machine Learning at Tulane University in the Spring of 2021. The application is currently maintained by Jack Strasburger. 

The application was almost exclusively written in python and is deployed using a variety of Amazon Web Services (Elastic Beanstalk, DynamoDb, S3, Lambda, Route 53, EC2 Instance, etc.). This deployment strategy is highly cost effective and lightweight, leading to rapid development and easy deployment. The full application can be viewed at nolaanalytics.com. 

### **AWS Utilized**
Our team utilized the following AWS Services:
1. **Elastic BeanStalk** (App Deployment)

2. **Cloud9** (Linux VM for resource creation)

3. **S3** (Storage and some static resources)

4. **Route 53** (DNS Routing)

5. **Lambda** (Automated Twitter API calls)

6. **DynamoDb** (Database)

7. **IAM** (Role Management)

<br>

### **Machine Learning Techniques**
The model we used was a linear Support Vector Classifier -  For more information on our model, please visit the model page of nolaanalytics.com/model. 


### **MIT License**

Copyright © 2021 Jack Strasburger

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the “Software”), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.