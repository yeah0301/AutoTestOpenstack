# coding=UTF-8
import urllib2
import urllib
import json
import datetime
import ConfigParser


class RESTfulSpiratest():

    def __init__(self,param):
         
        self.username = param['user']
        self.api_key = param['api_key']
        self.project_id = param['project_id']
        self.server = param['server']
        self.path = param['path']
        self.author_id = param['author_id']
        self.author_name = param['author_name']
         
        self.headers = { 'username' : self.username ,
           'api-key' : self.api_key,
           #'password':self.password,
           'Content-Type': 'application/json',
           'accept': 'application/json'}
    
        self.time = datetime.datetime

#     def __init__(self):
#          
#         self.username = 'AutoMan'
#         self.api_key = '{DBA6E463-DF98-43C9-B8A2-CC085BC9D858}'
#         self.project_id = 36
#         self.server = '140.96.27.65'
#         self.path = 'SpiraTest'
#          
#         self.headers = { 'username' : self.username ,
#            'api-key' : self.api_key,
#            'Content-Type': 'application/json',
#            'accept': 'application/json'}
    
     
#     def __init__(self):
#          
#         self.username = 'administrator'
#         self.api_key = '{52E26745-5AED-402F-A739-0A9271CB8010}'
#         self.project_id = 2
#         self.server = '140.96.29.146'
#         self.path = 'SpiraTest'
#          
#         self.headers = { 'username' : self.username ,
#            'api-key' : self.api_key,
#            #'password':self.password,
#            'Content-Type': 'application/json',
#            'accept': 'application/json'}
        
     
    def create_test_folder(self,name,parent_folder_id):
        
        #parent_test_folder_id 隨便填寫一個既有的ID
        url = ('http://{server}/{path}/Services/v4_0/RestService.svc/projects/{project_id}/test-folders'
               '?parent_test_folder_id={parent}'
               .format(server=self.server, 
                       path=self.path, 
                       project_id=self.project_id,
                       parent=parent_folder_id))
        

        values = ('{"ArtifactTypeId":2,'
                  '"ConcurrencyDate":"\/Date(1438929882094+0800)\/",'#Web application exception
                  '"CustomProperties":null,'
                  '"ProjectId":'+ str(self.project_id) +','
                  '"Active":true,'
                  '"AuthorId":'+ self.author_id +','
                  '"AuthorName":"'+ self.author_name +'",'
                  '"AutomationAttachmentId":null,'
                  '"AutomationEngineId":null,'
                  '"CreationDate":"\/Date(1438929882094+0800)\/",'#Web application exception
                  '"Description":null,'
                  '"EstimatedDuration":null,'
                  '"ExecutionDate":null,'
                  '"ExecutionStatusId":null,'
                  '"Folder":true,'
                  '"IndentLevel":null,'
                  '"LastUpdateDate":"\/Date(1438929882094+0800)\/",'#Web application exception
                  '"Name":"'+ name +'",'
                  '"OwnerId":null,'
                  '"OwnerName":null,'
                  '"ProjectName":null,'
                  '"TestCaseId":null,'
                  '"TestCasePriorityId":null,'
                  '"TestCasePriorityName":null,'
                  '"TestSteps":null}'
                  )
        
        req = urllib2.Request(url, values,self.headers)       
        response = urllib2.urlopen(req)
        response.read()
        response.close()

    
    def create_test_case(self,name, folder_id):
        
        url = ('http://{server}/{path}/Services/v4_0/RestService.svc/projects/{project_id}/test-cases'
               '?parent_test_folder_id={folder}'
               .format(server=self.server, 
                       path=self.path, 
                       project_id=self.project_id,
                       folder=folder_id))
        
        
        values = ('{"ArtifactTypeId":2,'
                  '"ConcurrencyDate":"\/Date(1438929882094+0800)\/",'#Web application exception
                  '"CustomProperties":null,'
                  '"ProjectId":'+ str(self.project_id) +','
                  '"Active":true,'
                  '"AuthorId":'+ self.author_id +','
                  '"AuthorName":"'+ self.author_name +'",'
                  '"AutomationAttachmentId":null,'
                  '"AutomationEngineId":null,'
                  '"CreationDate":"\/Date(1438929882094+0800)\/",'#Web application exception
                  '"Description":null,'
                  '"EstimatedDuration":null,'#Minute
                  '"ExecutionDate":null,'
                  '"ExecutionStatusId":null,'
                  '"Folder":false,'
                  '"IndentLevel":null,'
                  '"LastUpdateDate":"\/Date(1438929882094+0800)\/",'#Web application exception
                  '"Name":"'+ name +'",'
                  '"OwnerId":null,'
                  '"OwnerName":null,'
                  '"ProjectName":null,'
                  '"TestCaseId":null,'
                  '"TestCasePriorityId":null,'
                  '"TestCasePriorityName":null,'
                  '"TestSteps":null}'
                  )
        
        
        #object transfer to string will happen error
        #I do not know why it happen  
        """
        data = {"ArtifactTypeId":2,
                "ConcurrencyDate":'/Date(-62135578800000-0500)/',
                "CustomProperties":None,
                "ProjectId":2,
                "Active":True,
                "AuthorId":'System Administrator',
                "AutomationAttachmentId":None,
                "AutomationEngineId":None,
                "CreationDate":"/Date(-62135578800000-0500)/",
                "Description":None,
                "EstimatedDuration":None,
                "ExecutionDate":None,
                "ExecutionStatusId":None,
                "Folder":False,
                "IndentLevel":None,
                "LastUpdateDate":'/Date(-62135578800000-0500)/',
                "Name":'auto_test_case_2',
                "OwnerId":None,
                "OwnerName":None,
                "ProjectName":None,
                "TestCaseId":None,
                "TestCasePriorityId":None,
                "TestCasePriorityName":None,
                "TestSteps":None
                }

        values = json.dumps(data)
        values=values.replace('/','\/')
        print(values)
        """
        
        req = urllib2.Request(url, values,self.headers)       
        response = urllib2.urlopen(req)
        response.read()
        response.close()
    
    def get_test_cases(self):
        """
            Get all test cases from Spiratest by using RESTful 
            return all the name of test cases and id
        
        """
        
        result = {}
        result['Folder'] = {}
        result['Test_case'] = {}
        
        url = ('http://'+ self.server +'/'+ self.path 
        +'/Services/v4_0/RestService.svc/projects/'+ str(self.project_id)
        +'/test-cases/search?starting_row=1&number_of_rows=100')
        
        #data = urllib.urlencode(values)
        req = urllib2.Request(url, "",self.headers)
        response = urllib2.urlopen(req)
        the_page = response.read()
        response.close()
        print the_page
        test_case_list = json.loads(the_page)
        
        for test_case in test_case_list:
            #result[test_case['Name']] = test_case['TestCaseId']
            if test_case['Folder'] is True:
                result['Folder'][test_case['Name']] = test_case['TestCaseId']
            else:
                result['Test_case'][test_case['Name']] = test_case['TestCaseId']
        
        return result
    

    #TO DO : start date must be parameter
    #TO DO : end date must be parameter
    def create_release(self,name,version,startime,endtime):
        
        url = ('http://{server}/{path}/Services/v4_0/RestService.svc/projects/{project_id}/releases'
               .format(server=self.server, 
                       path=self.path, 
                       project_id=self.project_id))
        
        values =('{"ArtifactTypeId":4,'
                 '"ConcurrencyDate":"\/Date(1438929882094+0800)\/",'#The is web of office web is fuck, default Date(-62135578800000-0500) is overflow
                 '"CustomProperties":null,'
                 '"ProjectId":'+ str(self.project_id) +','
                 '"Active":true,'
                 '"AvailableEffort":null,'
                 '"CreationDate":"\/Date(1438929882094+0800)\/",' #Web application exception
                 '"CreatorId":'+ self.author_id +','
                 '"CreatorName":"'+ self.author_name +'",'
                 '"DaysNonWorking":0,'
                 '"Description":null,'
                 '"EndDate":"\/Date('+ endtime +'000)\/",'
                 '"FullName":"'+ version + ' - ' + name +'",'#format is VersionNumber - Name
                 '"IndentLevel":null,'
                 '"Iteration":false,'
                 '"LastUpdateDate":"\/Date(1438929882094+0800)\/",'
                 '"Name":"'+ name +'",'
                 '"PlannedEffort":null,'
                 '"ReleaseId":null,'
                 '"ResourceCount":0,'#I don't know 
                 '"StartDate":"\/Date('+ startime +'000)\/",'
                 '"Summary":false,'
                 '"TaskActualEffort":null,'
                 '"TaskCount":0,'
                 '"TaskEstimatedEffort":null,'
                 '"VersionNumber":"'+ version +'"}'
                 )
        
        try:
            req = urllib2.Request(url, values,self.headers)       
            response = urllib2.urlopen(req)
            return response.read()
        except urllib2.HTTPError as e:
            print e.reason,e.code
    
    
    def get_releases(self):
        
        url = ('http://{server}/{path}/Services/v4_0/RestService.svc/projects/{project_id}/releases'
               .format(server=self.server, 
                       path=self.path, 
                       project_id=self.project_id))
    
        result = {}
        
        try:
            req = urllib2.Request(url)
            for header in self.headers:
                req.add_header(header, self.headers[header])
            response = urllib2.urlopen(req)
            releases = json.loads(response.read())
            for release in releases:
                result[release['Name']] = release['ReleaseId']
                
            return result
        except urllib2.HTTPError as e:
            print e.reason,e.code
        
        
if __name__ == '__main__':
    config = ConfigParser.RawConfigParser(allow_no_value=True)
    config.read('config.cfg')
    
    restful = RESTfulSpiratest(dict(config.items('SpiraTest')))
    #restful.get_releases()
    #print json.loads(restful.create_release('test_rl3', 'str','',''))['ReleaseId']
    #print restful.get_test_cases()['Test_case'].values()[0]
    #restful.create_test_case('auto1', -1)
    #restful.create_test_folder('test')
    print restful.get_test_cases()
    #print restful.get_releases()
    
    
    
    