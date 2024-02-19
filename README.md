# Django Real Estate Backend Clone
I have replicated a Django backend from my previous company's private Git Repository, which I have since scrubbed of sensitive data and made publicly available on my GitHub account.

## Environment
- Django 4.1
- Python 3.9
- Ubuntu 20.04

## Project Structure
- User Management
-- Account creation
-- User authentication
-- Email verification
-- Google, Facebook OAuth integration
-- Role management for seven types of users
    > Django RESTful API - React.js - MUI Interface
- Advertisement
   Unique user roles have been developed for ad creation, distinct from regular site users. These users are tasked with creating select advertisements. An administration page facilitating the management of advertisements aids the marketing team, featuring images and respective descriptions.
     > Django API - Django Template
- Boost Marketing
   This feature promotes ads via advertising services.
    > Django API - Django Template
- Property Sale/Rent - Buy/Borrow
    Serving as the main feature of the site, this section equips users with options to sell, rent, buy or borrow property. Each account is tied to a specific user role. Property owners can detail properties for potential contract formation through the site. Meanwhile, prospective borrowers can filter and view available properties.
    > Django RESTful API - React.js - MUI
- Virtual Office
    This feature enables discussions around properties within a virtual space. Property owners can create these virtual offices and invite borrowers. Document exchange, along with signing, occur within this framework.
    > Django RESTful API - React.js – MUI

In addition to these, the project encompasses functionalities like neighborhood search or team management. This backend API, developed over five months from May to October 2023, is currently being maintained and updated in response to continuous client feedback.