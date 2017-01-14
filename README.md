## Living Cost Calculator - Kalkulator življenskih stroškov

The objective of this project is to create a Living Cost Calculator in order to help people who have dificulty in saving money, staying within budget or tracking expenses. This web application, called Budgeteer, will help users track their total accounts balances, set objetives and monitor individual accounts. i

## Target Audience

Everyone can use this web application, however it may be more useful for young people who need to set a budget and help them stick to it.

## Features

This web application will let you: 
- See your current balance.
- Track different accounts, wich will affect your total balance. For instance, you can have expenses in one account and receive money in the other, and the outcome will affect the total balance.
- See the graph of your balance for the past month.
- See the transactions you logged in the past month.
- Set objectives that will help you save money. They could be set up and different combinations can be made, such as: 
  - Have some total balance at the end of the month.
  - Save X money until the end of the month.
  
## Supported Devices and Browsers

This Web application will be supported by every mainstream and updated browser (Safari, MS Edge, Chrome, Opera,...) and will be mobile friendly. 

I have tested this web application in the following browsers:
- Google Chrome Version 54.0.2840.98 (64-bit)
- Safari Version 10.0.1 (12602.2.14.0.7)
- Mozilla Firefox Version 50.0

## How the Application is viewed in different Browsers

In this section we will analyse each page, as it is viewed by each tested browser.

#### index.html
  This is was meant to be a simple landing page for the application. As such, there is not much work done in terms of HTML & CSS and there is no JavaScript in use in this page. Therefore, there is no notorious difference between browsers, when viewing this page. However, we can see a slightly difference from Safari to the other two browsers in the placement of one of the headers. 
  
#### signup.html
  Also a simple page for signup. However, there are quite a few differences on how different browsers handle this page. In the signup form, all the fields are required and have the type that they should have. However, only Google Chrome enforces all of this requirements by not letting the form be submitted without email, password or password confirmation or by having an email that is not an email. Firefox also doesn't let the user submit the form without every field completed, however, the user can submit the form without having a proper email address. Safari doesn't enforce any of this requirements. As such, I've implemented regular expression verifiers for the email in JavaScript and I also make sure that the user has filled all the fields before submitting the form. I also verify if both the passwords match before submitting the form.
  
#### login.html
  Similar to signup.html but the user only has to submit the email and password. The requirements in this fields are the same as in the signup field, with browsers handling them in the same way. I also verify if the email is indeed in email format and if no fields are left empty with JavaScript.
  
#### dashboard.html
  The dashboard, like every page after loggin in, have a navbar, which is displayed in the same way in every different browser. It also has a table, which is also displayed in the same way for every browser. What doesn't display in the same way for every browser is my Add Expense form, which has an "Amount" field that accepts data of the type "Number", a "Description" field and an "Account" field, that accepts data of the type "text" and a "Date" field, that accepts data of the type "Date".
  Only Google Chromes enforces that a number and a date are entered in the fields with those data types. Both Safari and Firefox let you input text in those fields. As such, I had to verify the inputs with regular expressions to make sure that the user only inputs data of the permitted type. Safari also doesn't require the user to fill the fields, which should be an obligatory requirement. As such, I also verify if the fields have data before submitting. 
  In the second phase of the project I intend to draw a chart with dynamic data from the back-end so the user can follow is balance from the last monthes.
  
#### manageAccounts.html
  This page will let the user manage is accounts, by adding, deleting and editing accounts, which are displayed in a table. The user can edit the table directly, by pressing the "edit" button. This functionality is available and working in all the different browsers.
  There is also a form similar to the one in the dashboard.html, which had the same problems in the different browsers, which I handled in the same way.
  
#### manageObjectives.html
  This page will let the user set different objectives for his accounts or for his total balance. This objectives are also displayed in a table, in which the user will be able to delete, edit and add objectives.
  There is also a form, similar to the other forms that I mentioned above.
 
## Two features in which I invested more effort
  As the website is mainly consisted by tables, it was in those tables in which I invested more effort. In particular in this two features: 
  - Add data to the tables:
    The user is able to add data to the tables and they will change dynamically. This data is verified in order to make sure that is of the correct type and are the fields that are required are filled. However, as this is not yet saved in a database, when the page is refreshed all the changes are reseted. 
  - Edit data in the tables:
    The user is able to edit data in the tables, and the data will also change dynamically. However, as this is not yet saved in a database, when the page is refreshed all the changes are reseted.
   
## Objectives for the Second Phase
  My objectives for the second phase include:
  - Dynamic chart in the dashboard
  - Dynamic tables
  - Notifications when an objective is completed or failed
  - Log in with an API (Facebook or GMAIL)
  - And More!
  

