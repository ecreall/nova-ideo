*** Settings ***

Variables  pyramid_robot/tests/robot/variables.py

Library  Selenium2Library  timeout=${SELENIUM_TIMEOUT}  implicit_wait=${SELENIUM_IMPLICIT_WAIT}

#Resource  Selenium2Screenshots/keywords.robot

Suite Setup  Suite Setup
Suite Teardown  Suite Teardown

*** Keywords ***

Suite Setup
  Open browser  ${APP_URL}  browser=${BROWSER}  remote_url=${REMOTE_URL}  desired_capabilities=${DESIRED_CAPABILITIES}

Suite Teardown
  Close All Browsers

I go to
    [Arguments]  ${location}
    Go to  ${location}

Create an account
    I go to  ${APP_URL}
    Click link  id=registration
    Click element  xpath=//span[text()='- Select -']
    Click element  xpath=//ul[@class='select2-results']/li[div/text()='Madam']
    Input text  first_name  Helene
    Input text  last_name  Dupont
    Input text  email  helenedupont@example.com
    Input text  xpath=//ul[@class='select2-choices']/li/input  espaces naturels
    Click element  xpath=//span[text()='espaces naturels']
    Input text  name=password  0000
    Input text  name=password-confirm  0000
    Click button  name=User_registration

Login as helene
    I go to  ${APP_URL}
    Click link  id=log-in
    Input text  email  helenedupont@example.com
    Input text  name=password  0000
    Click button  Log In

*** Test cases ***

Scenario: Test Homepage
    Create an account
    Login as helene
    Page should contain  0 elements trouv

Scenario: Test Menu
    I go to  ${APP_URL}
    Page should contain  Search
    Page should contain  Idea
    Page should contain  Person
    Page should contain  Proposal
    Click element  xpath=//span[text()='ON']
    Page Should Contain  Search
    Page Should Not Contain Element  Idea
    Page Should Not Contain Element  Person
    Page Should Not Contain Element  Proposal

Scenario: Login with wrong password
    Create an account
    I go to  ${APP_URL}
    Click link  id=log-in
    Input text  email  helenedupont@example.com
    Input text  name=password  1111
    Click button  Log In
    Page should contain  Failed login

#Scenario: Get a new password
#   Pour l'instant on ne peut pas récupérer de mot de passe

