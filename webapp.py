import os
from flask import Flask, request
from flask.ext import restful

import httplib
import logging
import requests

import beatbox

from restmarketo import Client

app = Flask(__name__)
api = restful.Api(app)


# this code doesn't work -- but it is a rough outline of the steps the merge script should take.
class Merge(restful.Resource):
    def post(self):
        #1. get posted data from Architizer web app.
        json_input = request.get_json(force=True)
        email = str(json_input)

        #2. connect to salesforce instance
        svc = beatbox.PythonClient()
        svc.login('username', 'passwordToken')

        #3. Query SFDC contact table
        contactEmails = svc.query("SELECT * FROM Contact WHERE Email=Email")

        #4. Check if those contacts in SFDC match the new email that was posted to this API
        for e in contactEmails:
            if email == e:
                # 4.a check if account of that contact is architizer User
                account = svc.query("SELECT AccountName from ACCOUNT where Email=e")
                if account = 'Architizer User':
                    # Do some logic
                    mergedarchitizeruser = True # this will be used for something later.
                    break
                else:
                    #4.b - account is not architizer user, merge as normal
            # set flag that we merged a contact
            mergedcontact = True
            break

        if not mergedcontact:
            #5. get Leads in SFDC
            leadEmails = svc.query("SELECT * FROM Lead WHERE Email=Email")

            for e in leadEmails:
                if email == e:
                    # merge
                    # then break
                    # set flag that we merged a contact
                    mergedlead = True
                    break

        # 6. no matches found - create new contact

        if not mergedcontact or mergedarchitizeruser or mergedlead:
            # create a new contact in SFDC

        return True


api.add_resource(Merge, '/merge')

if __name__ == '__main__':
    app.run(debug=True)
    print 'app loaded'
