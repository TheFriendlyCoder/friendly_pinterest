Overview
=============

User friendly Python wrapper for the
`Pinterest developer APIs <https://developers.pinterest.com/>`_.
This project is currently in very early development, with only a bare minimum
of functionality, intended for some of my personal projects. I'm sharing it here
in case someone finds the implementation helpful for their projects. Also, if
anyone would like to contribute to this pet project feel free to fork it and
send me pull requests for any changes you may like.

Comments, suggestions and bugs may be reported to the project
`maintainer <mailto:thefriendlycoder@gmail.com>`_

Full API documentation can be found on
`ReadTheDocs.org <http://friendlypins.readthedocs.io/en/latest/>`_.

Development Environment
=======================

In order to make use of this library, you will need a private access token
to use when instantiating the main api class. This token authenticates you
as a specific Pinterest user, giving access to that users' profile, boards
and pins. Typically this token would be generated by an application, but for
testing purposes you can manually generate a token as described below. These
steps are loosley based on the steps described on the
`Developer API <https://developers.pinterest.com/docs/api/overview/>`_
under the "Postman" app section.

1. Navigate to the Pinterest developer website and sign up for a free account:
   https://developers.pinterest.com
2. Under your personal profile, click the "Create App" button
3. Name your app something appropriate like "My Test App"
4. Once you create your test app, you'll need to set up a "Platform". Under
   the "Web" platform enter: https://www.getpostman.com/oauth2/callback
5. Download and install Postman app for your platform: https://www.getpostman.com/apps
6. When you launch the app, you'll be prompted to set up a free account. Either
   set up a free account or choose the "skip" link at the bottom of the page.
7. Click the "new request" button on the wizard that pops up
8. enter a name for your config (ie testing)
9. click create collection and give it a name (ie my collection)
10. click save
11. in the “get” field enter a Pinterest rest api endpoint url like:
    https://api.pinterest.com/v1/me/pins
12. under “Authorization -> type” select oauth 2.0
13. under "Add authorization data to” select “request url”
14. click “get new access token”
15. fill out the form that pops up as follows:

    * grant type: authorization code
    * callback url: https://www.getpostman.com/oauth2/callback
    * auth url: https://api.pinterest.com/oauth
    * access token url: https://api.pinterest.com/v1/oauth/token
    * clientID: app ID from your pinterest app created above
    * client secret: app secret also from your pinterest app
    * scope: read_public,write_public,read_relationships,write_relationship
    * state: leave blank
    * client authentication: send as basic auth header

16. click request token
17. you’ll be redirected to pinterest web site. Log in as yourself.
18. when prompted, click “okay”to allow your test app access to your pinterest
    account
19. click “use token"
20. The token will appear in the collection configuration. Copy the token from
    there and paste it into your script or pass it along to the calls to `fpins`
    on the console.

