# keydom.py


<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a id="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->

<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![Twitter][twitter-shield]][twitter-url]


<!-- PROJECT LOGO -->
<br />
<div align="center">
  <h3 align="center">keydom.py</h3>

  <p align="center">
    Tools to interact with Keydom Access Control System from FAAC
    <br />
    <a href="https://github.com/drcoccodrillus/keydompy/issues">Report Bug</a>
  </p>
</div>


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#introduction">Introduction</a>
        <ul>
            <li><a href="#about-the-project">About the project</a></li>
            <li><a href="#who-should-use-this-package">Who should use this package</a></li>
        </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#package-installation">Package installation</a></li>
        <li><a href="#environment-variables">Environment variables</a></li>
        <li>
            <a href="#package-usage">Package usage</a>
            <ul>
                <li><a href="#user-management">User management</a></li>
                <li><a href="#access-media-management">Access media management</a></li>
                <li><a href="#visit-management">Visit management</a></li>
                <li><a href="#presence-management">Presence management</a></li>
            </ul>
        </li>
      </ul>
    </li>
    <li><a href="#license">License</a></li>
    <li><a href="#contacts">Contacts</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>


<a id="introduction"></a>

## Introduction

<a id="about-the-project"></a>

### About The Project

Keydom is an access control system developed by [FAAC](https://faac.it/). keydom.py provides a set of commands to interact with the Keydom system.


<a id="who-should-use-this-package"></a>

### Who should use this package

This package is intended for developers who need to interact with the Keydom system from FAAC. Any developer who needs to manage users, doors, and access rights in a Keydom system can use this package.


<p align="right">(<a href="#readme-top">go to top</a>)</p>


<a id="getting-started"></a>

## Getting Started

<a id="prerequisites"></a>

### Prerequisites

- Python 3.6 or higher
- pip

<a id="package-installation"></a>

### Package installation

- Use pip to install the pre-builded package `pip install keydom`

<a id="environment-variables"></a>

### Environment variables

You can set the following environment variables to configure the connection to the Keydom system:

```
export KEYDOM_PROTOCOL=https
export KEYDOM_IP=172.26.20.120
export KEYDOM_PORT=443
export KEYDOM_USERNAME=admin
export KEYDOM_PASSWORD=admin
```

<a id="package-usage"></a>

### Package usage

First thing you need to do is to import the package:

`from keydom import KeydomManager`

Then you can create an instance of `KeydomManager`:

`km = KeydomManager()`

Now you are ready to use the following methods and interact with the Keydom system:


<a id="user-management"></a>

### USER MANAGEMENT

<p align="right">(<a href="#access-media-management">go to access media management</a>)</p>

`insert_internal()`

Parameters:
- `first_name` (str): The first name of the user
- `last_name` (str): The last name of the user
- `qualification` (str): The qualification of the user (a tag that can be used to filter users)
- `registration_number` (str): The registration number of the user
- `address` (str): The address of the user
- `phone` (str): The phone number of the user
- `mobile` (str): The mobile number of the user
- `email` (str): The email of the user
- `notes` (str): A note about the user

Usage examples:

```
km.insert_internal()    # Insert a new anonimous user
km.insert_internal(first_name='John', last_name='Doe')
km.insert_internal(first_name='John', last_name='Doe', qualification='employee')
km.insert_internal(first_name='John', last_name='Doe', qualification='employee', registration_number='123456')
km.insert_internal(first_name='John', last_name='Doe', qualification='employee', registration_number='123456', address='Ricketts Road, Mount Waverley VIC 3149, Australia')
```

`update_internal()`

Parameters:
- `uuid` (int): The ID of the user
- `first_name` (str): The first name of the user
- `last_name` (str): The last name of the user
- `qualification` (str): The qualification of the user (a tag that can be used to filter users)
- `registration_number` (str): The registration number of the user
- `address` (str): The address of the user
- `phone` (str): The phone number of the user
- `mobile` (str): The mobile number of the user
- `email` (str): The email of the user
- `notes` (str): A note about the user

Usage examples:

```
km.update_internal(1, first_name='John', last_name='Doe')   # Update the user with ID 1
km.update_internal(1, first_name='John', last_name='Doe', qualification='employee')
km.update_internal(1, first_name='John', last_name='Doe', qualification='employee', registration_number='123456')
km.update_internal(1, first_name='John', last_name='Doe', qualification='employee', registration_number='123456', address='Ricketts Road, Mount Waverley VIC 3149, Australia')
```

`insert_visitor()`

Parameters:
- `first_name` (str): The first name of the visitor
- `last_name` (str): The last name of the visitor
- `qualification` (str): The qualification of the visitor (a tag that can be used to filter visitors)
- `registration_number` (str): The registration number of the visitor
- `address` (str): The address of the visitor
- `phone` (str): The phone number of the visitor
- `mobile` (str): The mobile number of the visitor
- `email` (str): The email of the visitor
- `document_number` (str): The document number of the visitor

Usage examples:

```
km.insert_visitor()    # Insert a new anonimous visitor
km.insert_visitor(first_name='John', last_name='Doe')
km.insert_visitor(first_name='John', last_name='Doe', qualification='visitor')
km.insert_visitor(first_name='John', last_name='Doe', qualification='visitor', registration_number='123456')
km.insert_visitor(first_name='John', last_name='Doe', qualification='visitor', registration_number='123456', address='Ricketts Road, Mount Waverley VIC 3149, Australia')
```

`update_visitor()`

Parameters:
- `uuid` (int): The ID of the visitor
- `first_name` (str): The first name of the visitor
- `last_name` (str): The last name of the visitor
- `qualification` (str): The qualification of the visitor (a tag that can be used to filter visitors)
- `registration_number` (str): The registration number of the visitor
- `address` (str): The address of the visitor
- `phone` (str): The phone number of the visitor
- `mobile` (str): The mobile number of the visitor
- `email` (str): The email of the visitor
- `document_number` (str): The document number of the visitor

Usage examples:

```
km.update_visitor(1, first_name='John', last_name='Doe')   # Update the visitor with ID 1
km.update_visitor(1, first_name='John', last_name='Doe', qualification='visitor')
km.update_visitor(1, first_name='John', last_name='Doe', qualification='visitor', registration_number='123456')
km.update_visitor(1, first_name='John', last_name='Doe', qualification='visitor', registration_number='123456', address='Ricketts Road, Mount Waverley VIC 3149, Australia')
```

`insert_business()`

Parameters:
- `name` (str): The name of the business
- `address` (str): The address of the business
- `phone` (str): The phone number of the business
- `mobile` (str): The mobile number of the business
- `fax` (str): The fax number of the business
- `email` (str): The email of the business
- `notes` (str): A note about the business

Usage examples:

```
km.insert_business()    # Insert a new anonimous business
km.insert_business(name='ACME Inc.')
km.insert_business(name='ACME Inc.', address='Ricketts Road, Mount Waverley VIC 3149, Australia')
km.insert_business(name='ACME Inc.', address='Ricketts Road, Mount Waverley VIC 3149, Australia', phone='123456')
```

`update_business()`

Parameters:
- `uuid` (int): The ID of the business
- `name` (str): The name of the business
- `address` (str): The address of the business
- `phone` (str): The phone number of the business
- `mobile` (str): The mobile number of the business
- `fax` (str): The fax number of the business
- `email` (str): The email of the business
- `notes` (str): A note about the business

Usage examples:

```
km.update_business(1, name='ACME Inc.')   # Update the business with ID 1
km.update_business(1, name='ACME Inc.', address='Ricketts Road, Mount Waverley VIC 3149, Australia')
km.update_business(1, name='ACME Inc.', address='Ricketts Road, Mount Waverley VIC 3149, Australia', phone='123456')
```

`delete_user()`

Parameters:
- `uuid` (int): The ID of the user

Usage examples:

```
km.delete_user(1)   # Delete the user with ID 1
```

`delete_by_type_user()`

Parameters:
- `type` (str): The type of the user (internal, visitor, business)

Usage examples:

```
km.delete_by_type_user(0)   # Delete all internal users
km.delete_by_type_user(1)   # Delete all visitors
km.delete_by_type_user(2)   # Delete all businesses
```

<p align="right">(<a href="#user-management">go to user management</a>)</p>


<a id="access-media-management"></a>

### ACCESS MEDIA MANAGEMENT

<p align="right">(<a href="#visit-management">go to visit management</a>)</p>

<a id="insert-access-media"></a>

`insert_access_media()`

Parameters:
- `uuid` (str): The ID of the access media
- `identifier` (str, required): The identifier of the access media
- `mediaTypeCode` (int): The type of the access media
- `number` (str): The number of the access media
- `enabled` (bool): If the access media is enabled
- `validityStart` (str): The start date of the validity of the access media
- `validityEnd` (str): The end date of the validity of the access media
- `validityMode` (int): The mode of the validity of the access media
- `antipassbackEnabled` (bool): If the access media has the antipassback feature enabled
- `countingEnabled` (bool): If the access media has the counting feature enabled
- `userUuid` (int): The ID of the user that owns the access media
- `profileUuidOrName` (int): The ID or the name of the profile of the access media
- `lifeCycleMode` (int): The mode of the life cycle of the access media
- `relatedAccessMediaNumber` (str): The number of the related access media

Usage examples:

```
km.insert_access_media(identifier='123456')
```

<a id="update-access-media"></a>

`update_access_media()`

Parameters:
- `uuid` (str, required): The ID of the access media
- `identifier` (str, required): The identifier of the access media
- `mediaTypeCode` (int): The type of the access media
- `number` (str): The number of the access media
- `enabled` (bool): If the access media is enabled
- `validityStart` (str): The start date of the validity of the access media
- `validityEnd` (str): The end date of the validity of the access media
- `validityMode` (int): The mode of the validity of the access media
- `antipassbackEnabled` (bool): If the access media has the antipassback feature enabled
- `countingEnabled` (bool): If the access media has the counting feature enabled
- `userUuid` (int): The ID of the user that owns the access media
- `profileUuidOrName` (int): The ID or the name of the profile of the access media
- `lifeCycleMode` (int): The mode of the life cycle of the access media
- `relatedAccessMediaNumber` (str): The number of the related access media

Usage examples:

```
km.update_access_media('63d59ede-62b2-427f-877a-1a28197c2a71', identifier='998877')
```

<a id="enable-access-media"></a>

`enable_access_media()`

Parameters:
- `uuid` (str, required): The ID of the access media

Usage examples:

```
km.enable_access_media('63d59ede-62b2-427f-877a-1a28197c2a71')
```

<a id="disable-access-media"></a>

`disable_access_media()`

Parameters:
- `uuid` (str, required): The ID of the access media

Usage examples:

```
km.disable_access_media('63d59ede-62b2-427f-877a-1a28197c2a71')
```

<a id="unlink-access-media"></a>

`unlink_access_media()`

Parameters:
- `uuid` (str, required): The ID of the access media

Usage examples:

```
km.unlink_access_media('63d59ede-62b2-427f-877a-1a28197c2a71')
```

<a id="get_access_media_uuid"></a>

`get_access_media_uuid()`

Parameters:
- `number` (str, required): The number of the access media

Usage examples:

```
km.get_access_media_uuid('99133')
```

<a id="get_access_media_identifier"></a>

`get_access_media_identifier()`

Parameters:
- `number` (str, required): The number of the access media

Usage examples:

```
km.get_access_media_identifier('99133')
```

<a id="update_balance_access_media"></a>

`update_balance_access_media()`

Parameters:
- `uuid` (str, required): The ID of the access media
- `balance` (int, required): The balance of the access media

<p align="right">(<a href="#access-media-management">go to access media management</a>)</p>


<a id="visit-management"></a>

### VISIT MANAGEMENT

<p align="right">(<a href="#presence-management">go to presence management</a>)</p>

<a id="get_created_visits"></a>

`get_created_visits()`

Parameters:
- `pageIndex` (str): The index of the page
- `pageSize` (str): The size of the page

Usage examples:

```
km.get_created_visits()
km.get_created_visits(pageSize=1000)
km.get_created_visits(pageIndex=3, pageSize=1000)
```

<a id="get_in_progress_visits"></a>

`get_in_progress_visits()`

Parameters:
- `pageIndex` (str): The index of the page
- `pageSize` (str): The size of the page

Usage examples:

```
km.get_in_progress_visits()
km.get_in_progress_visits(pageSize=1000)
km.get_in_progress_visits(pageIndex=3, pageSize=1000)
```

<a id="get_completed_visits"></a>

`get_completed_visits()`

Parameters:
- `pageIndex` (str): The index of the page
- `pageSize` (str): The size of the page

Usage examples:

```
km.get_completed_visits()
km.get_completed_visits(pageSize=1000)
km.get_completed_visits(pageIndex=3, pageSize=1000)
```

<a id="get_all_visits"></a>

`get_all_visits()`

Parameters:
- `pageIndex` (str): The index of the page
- `pageSize` (str): The size of the page

Usage examples:

```
km.get_all_visits()
km.get_all_visits(pageSize=1000)
km.get_all_visits(pageIndex=3, pageSize=1000)
```

<a id="get_visit_details"></a>

`get_visit_details()`

Parameters:
- `uuid` (str, required): The ID of the visit

Usage examples:

```
km.get_visit_details('5ac536d6-426b-4bf3-add6-d87f7c917557')
```

<a id="insert_visit"></a>

`insert_visit()`

Parameters:
- `userUuid` (str, required): The ID of the visitor
- `uuid` (str): The ID of the visit
- `start` (str): The start date of the visit
- `end` (str): The end date of the visit
- `field1` (str): The first field of the visit
- `field2` (str): The second field of the visit
- `field3` (str): The third field of the visit
- `notes` (str): A note about the visit

Usage examples:

```
km.insert_visit('1')
```

<a id="delete_visit"></a>

`delete_visit()`

Parameters:
- `uuid` (str, required): The ID of the visit

Usage examples:

```
km.delete_visit('4c864fc4-e952-4141-abdf-0848dc0e2f05')
```

<a id="open_visit"></a>

`open_visit()`

Parameters:
- `uuid` (str, required): The ID of the visit

Usage examples:

```
km.open_visit('4c864fc4-e952-4141-abdf-0848dc0e2f05')
```

<a id="close_visit"></a>

`close_visit()`

Parameters:
- `uuid` (str, required): The ID of the visit

Usage examples:

```
km.close_visit('4c864fc4-e952-4141-abdf-0848dc0e2f05')
```

<p align="right">(<a href="#visit-management">go to visit management</a>)</p>


<a id="presence-management"></a>

### PRESENCE MANAGEMENT

<a id="get_presences"></a>

`get_presences()`

Parameters:
- `pageIndex` (str): The index of the page
- `pageSize` (str): The size of the page

Usage examples:

```
km.get_presences()
km.get_presences(pageSize=1000)
km.get_presences(pageIndex=3, pageSize=1000)
```

<a id="get_presences_emergency_points"></a>

`get_presences_emergency_points()`

Parameters:
- `pageIndex` (str): The index of the page
- `pageSize` (str): The size of the page

Usage examples:

```
km.get_presences_emergency_points()
km.get_presences_emergency_points(pageSize=1000)
km.get_presences_emergency_points(pageIndex=3, pageSize=1000)
```

<p align="right">(<a href="#presence-management">go to presence management</a>)</p>


<a id="license"></a>

## License

Distributed under the Apache License. See `LICENSE` for more information.


<p align="right">(<a href="#readme-top">go to top</a>)</p>


<a id="contacts"></a>

## Contacts

drcoccodrillus - [@DrCoccodrillus](https://twitter.com/DrCoccodrillus)

Project Link: [https://github.com/drcoccodrillus/keydompy](https://github.com/drcoccodrillus/keydompy)


<p align="right">(<a href="#readme-top">go to top</a>)</p>


<a id="acknowledgments"></a>

## Acknowledgments

* [FAAC](https://faac.it/)
* [Choose an Open Source License](https://choosealicense.com)
* [Img Shields](https://shields.io)
* [GitHub Pages](https://pages.github.com)


<p align="right">(<a href="#readme-top">go to top</a>)</p>


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/drcoccodrillus/keydompy.svg?style=for-the-badge
[contributors-url]: https://github.com/drcoccodrillus/keydompy/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/drcoccodrillus/keydompy.svg?style=for-the-badge
[forks-url]: https://github.com/drcoccodrillus/keydompy/network/members
[stars-shield]: https://img.shields.io/github/stars/drcoccodrillus/keydompy.svg?style=for-the-badge
[stars-url]: https://github.com/drcoccodrillus/keydompy/stargazers
[issues-shield]: https://img.shields.io/github/issues/drcoccodrillus/keydompy.svg?style=for-the-badge
[issues-url]: https://github.com/drcoccodrillus/keydompy/issues
[license-shield]: https://img.shields.io/github/license/drcoccodrillus/keydompy.svg?style=for-the-badge
[license-url]: https://github.com/drcoccodrillus/keydompy/blob/main/LICENSE
[twitter-shield]: https://img.shields.io/twitter/url?url=https%3A%2F%2Ftwitter.com%2FDrCoccodrillus&style=for-the-badge&logo=x
[twitter-url]: https://twitter.com/DrCoccodrillus
[product-screenshot]: static/images/screenshot.png
