#encoding=UTF8
import urllib2
import json
import sys


class RESTfulJenkins():
    
    def __init__(self,server,port):
        self.server = server + ':' + str(port)
        self.headers = {'Content-Type': 'application/xml'}
    
    def create_job(self,job_name, description='', command=''):
        
        try:
            url = ('http://'+self.server+'/createItem?name='+ job_name)
            
            config = ('<project><actions/>'
            '<description>'+ description +'</description>'
            '<keepDependencies>false</keepDependencies>'
            '<properties><hudson.model.ParametersDefinitionProperty><parameterDefinitions>'
            '<hudson.model.StringParameterDefinition>'
            '<name>releaseName</name>'
            '<description></description>'
            '<defaultValue></defaultValue>'
            '</hudson.model.StringParameterDefinition>'
            '</parameterDefinitions></hudson.model.ParametersDefinitionProperty></properties>'
            '<scm class="hudson.scm.NullSCM"/>'
            '<canRoam>true</canRoam>'
            '<disabled>false</disabled>'
            '<blockBuildWhenDownstreamBuilding>false</blockBuildWhenDownstreamBuilding>'
            '<blockBuildWhenUpstreamBuilding>false</blockBuildWhenUpstreamBuilding>'
            '<triggers/>'
            '<concurrentBuild>false</concurrentBuild>'
            '<builders><hudson.tasks.Shell>'
            '<command>'+ command +'</command>'
            '</hudson.tasks.Shell></builders><publishers/><buildWrappers/></project>')
            
        except KeyError:
            KeyError.message

        req = urllib2.Request(url, config ,self.headers)
        response = urllib2.urlopen(req)
        response.read()
        response.close()
        
    def get_jobs_list(self):
        
        url = ('http://'+self.server+'/api/json?pretty=true')
        req = urllib2.Request(url, "" ,self.headers)
        response = urllib2.urlopen(req)
        
        if response.code == 200:
            jobs = json.loads(response.read())['jobs']
            response.close()
            return jobs
        else:
            response.close()
            sys.exit('ERROR : DO NOT GET Jenkins {} Jobs list '.format(self.server))
                
            
    def update_job(self,job ,description='', command=''):
        
        url = ('http://'+self.server+'/job/'+ job + '/config.xml')
        
        config = ('<project><actions/>'
            '<description>'+ description +'</description>'
            '<keepDependencies>false</keepDependencies>'
            '<properties><hudson.model.ParametersDefinitionProperty><parameterDefinitions>'
            '<hudson.model.StringParameterDefinition>'
            '<name>releaseName</name>'
            '<description></description>'
            '<defaultValue></defaultValue>'
            '</hudson.model.StringParameterDefinition>'
            '</parameterDefinitions></hudson.model.ParametersDefinitionProperty></properties>'
            '<scm class="hudson.scm.NullSCM"/>'
            '<canRoam>true</canRoam>'
            '<disabled>false</disabled>'
            '<blockBuildWhenDownstreamBuilding>false</blockBuildWhenDownstreamBuilding>'
            '<blockBuildWhenUpstreamBuilding>false</blockBuildWhenUpstreamBuilding>'
            '<triggers/>'
            '<concurrentBuild>false</concurrentBuild>'
            '<builders><hudson.tasks.Shell>'
            '<command>'+ command +'</command>'
            '</hudson.tasks.Shell></builders><publishers/><buildWrappers/></project>')
        
        
        req = urllib2.Request(url, config,self.headers)
        response = urllib2.urlopen(req)
        response.read()
        response.close()
        
        if response.code == 200:
            return True
        else:
            return False
        
        
if __name__ == '__main__':
    
    param = {}
    param['server'] = '10.206.20.1'
    param['port'] = 8081
    
    rest = RESTfulJenkins('10.206.20.1',8081)
    #rest.update_job('update_test', '123', '123')
    #rest.create_job()
    print rest.get_jobs_list()
    
    
