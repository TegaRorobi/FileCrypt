## Database Models & Notes on their  Functionality
**User**
- full name, email, password (email and password for authentication). 
- could just be a regular user, an individual making use of the service
- organisations, workspaces and teams they belong to
- upload sizes, number of encryption keys, number of available algorithms, etc. users can always upgrade this on a subscription model

<br>

**Business**
- name, email, address
- user account that created this business
- has the ability to create organisations

<br>

**Organisation**
- name, email, address
- has the ability to create workspaces

<br>

**Workspace**
- organisation which it belongs to
- the users in this workspace
- a workspace had access to certain encrypted files

<br>

**Team**
- team name, creator of this team
- workspace this team belongs to
- the users in this team
- there should be functionality for users to invite other users to their team
- each user within a team has individual authentication

<br>

**EncryptedFile, EncryptedFolder**
- filename, filetag or an identifier for this resource
- entity that uploaded this resource
- the encryption key(s) associated with this resource 
- the teams, workspaces, organisations, businesses, users that have access to this resource
- the actual encrypted content of the file
- upload, modification timestamps
- info about the encryption (algorithm, encryption key used, etc.)
- encrypted folders have to maintain the initial folder structure even after encryption
- paid users can select the encryption algorithm they wish to use
- when decrypting, the encryption key is provided and if it matches, the file is decrypted. there are various options for viewing the contents of the resource, like temporary links and ability to donwload the resource. the person sharing the file has access to determine how the file is viewed
- users receive alerts for various actions, including file access activity
- when a file is shredded, the encryption key of the file is deleted, rendering the file irrecoverable. on the backend, there is a check to make sure there is an EncryptionKey object associated with the value provided. if there isn't, then it would not even attempt to decrypt the file with the provided value

<br>

**EncryptionKey**
- the actual key
- the creator of this key
- the usage records of this key
- the usage limits of this key (number of times of total usage, number of usages per person it is shared to,)
- creation and use timestamps
- there would be activity tracking for everytime this key is used to decrypt a resource
- there should be functionality that allows users to share the encryption key to someone. this would need the owner to provide the email of the person they would like to share the encryption key with, and then on the backend, we would send an email to this person and when they create an account on the platform, they would be able to use the encryption key to access resources. with this, even if an encryption key is leaked, as long as they don't have access to an account the owner of the encryption key shared this key to, they would not still be able to use the key
- hence, the accounts that can make use of this encryption key (this would be gotten from another field, the EncryptionKeyRule, which allows to separate the usage restrictions per user this encryption key is shared to)

**EncryptionKeyRule**
- the encryption key
- the user that can make use of this encryption key via this rule
- the usage restrictions of the encryption key

<br>

## Additional notes

- there should be functionality for users to generate strong passwords with a password generator implemented on the backend
- email processing, encryption and decryption tasks should run asynchronously (Celery)

## System Architecture

The File Encryption System follows a modular monolithic architecture. Key components include:

1. **Django REST Framework:**
   - Used for building the RESTful API.

2. **Redis:**
   - Acts as a message broker for Celery.

3. **Celery:**
   - Manages asynchronous tasks such as encryption and email processing.

4. **PostgreSQL:**
   - Serves as the relational database for storing user data, encrypted content, and metadata.

5. **Silk:**
   - Provides performance monitoring and profiling for Django applications.

6. **DataDog:**
   - Integrated for comprehensive monitoring, alerting, and analytics.

   