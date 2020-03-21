# automateGmailReportMac
A project to get the list of all new (g)mails received in last 24 hours using python, automator and Mac.

Steps:
1.	Enable gmail API to download ‘credentials.json’.
2.	Install python packages for Google Client Library using the below command:

pip install –-user --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib Django

3.	Write a script to get the list of unread emails received in last 24 hours
4.	Analyze the result to prepare report
5.	Use Automator to read out the report
