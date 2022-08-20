# Let's bid
#### Video Demo:<https://youtu.be/CcDExCIDIiA>
#### Description:
**About:** This project allows user to bid for the product which will be available on website so basically this is a web application, made by me using python,flask,jinja,html,css.

**Login:** Application starts with login page where i have added a paragraph about bidding and i have added the source of paragraph for more refrence. After that user of this application is asked to login using their username and password. If user doesn't have username and password then  there is **Register** button available to register on site.

**Register**: In register route user is asked for username and password with confirmation of password. After register user will be  redirected to **login** page for login.

**Both** the register and login page inherits base.html
. If user tries to submit any form using post method without writing or skipping any field he will get error for the same. For example if user tries to login without entering username or password then user will get error that respective field cannot be empty. If user tries to register with already taken username then user will be prompted error.

**After Register and Login**: User will be directed to index page where user can see Bid Winner,History,links,product and logout in navigation bar. And Product available to bid in body part of index and form to place bid.

**Bidding**: User will be asked their username,Product,bid price in form then there will be one check box to read and accept the terms and condition. After filling the form user can submit the form. All fields are mandatory in this form, user will get error for any empty field. **Also User cannot place bid price lower than base price which will be displayed in the same page.**

**History**: After submitting the bid form user will be redirected to history page where user can see all the bids placed including the details of bidders and their price.

**Bid Winner**: In navigation bar there is a bid winner item which will show the current winning person,user bid price,and date of bidding of that bid (**This page will be displayed differently to the user who won the bid.**)

**Winner**: Winner page is designed only for winner of Auction . If same user who won the bid is login then winner page will ask for delivery address and payment mode is mentioned. And winner has to submit their details like email,name and address after the submit of address form **same user will be displayed a sold page where  no product will be visible as product is already sold**

**Adding**: This application has facility of logout and login again . User's data is secured as i am not storing their actual password, their password is stored in **hashed** form
there is one database **(database.db)** in which there are 3 tables which stores the user information. Also adding to security part user cannot route to any page without login.All html files are in templates section and in static folder i have added css file and required images which contribute in layout and base.html
python codes are written in **app.py**

