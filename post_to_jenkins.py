#coding=UTF-8
import restful_jenkins
import tempest_util
import datetime
from time import sleep
import ConfigParser
import os


class PostToJenkins():
    """
        Parser the test case of OpenStack Tempest from Tempest folder
        Default Tempest folder path is /opt/stack/tempest
        Then,  python will create jobs in Jenkins according to the test case
        
        Jobs which created in Jenkins formatter default
        Jobs name is the class name in the python file of Tempest
        The dscription of job is the set of function in class and its annotation
        The command of job is shell script.
        
    """
    
    def __init__(self):
        
        #Initial the config 
        self.config = ConfigParser.RawConfigParser(allow_no_value=True)
        self.config.read('config.cfg')
        
        #Initial Jenkins IP and port and Jenkins connect Object
        self.post = restful_jenkins.RESTfulJenkins(self.config.get('Jenkins','server')
                                                   ,int(self.config.get('Jenkins','port')))
        self.jobs = self.post.get_jobs_list()
        
        self.reps = {'\\':'.', '.py':'', 'tempest.tempest':'tempest','/':'.'}
        
        self.post_to_jenkins_log = []
        
        
    def create_one_job(self,path):
        
        self.path = path
        
        self.json = tempest_util.parser_test_case_return_json(self.path)
        
        time = datetime.datetime
        
        #universal name
        for rep in self.reps:
            self.path = self.path.replace(rep,self.reps.get(rep))
        
        if self.is_existed_job(self.path) == False :
            
            desc = 'PATH: {}\n'\
                'CREATED: {}\n'\
                '--------------------\n'\
                .format(self.path,time.now().strftime("%Y-%m-%d %H:%M:%S"))
            
            for file_path in self.json:
                desc += '[' + file_path + ']\n'
                for cls in self.json[file_path]:
                #Add function name in class and its annotation to the description
                    for func in self.json[file_path][cls]['func'].keys():
                        desc += '    ' + cls + '::' +func+'\n'
                        """
                        for tmp in self.json[file_path][cls]['func'][func].get('annotation','').split(','):
                            desc += '        ' + tmp + '\n'
                        desc += '\n'
                        """
                        
            cmd = 'cd /opt/stack/tempest\n'\
            'file=TempestLog/`date +%s`.log\n'\
            './run_tempest.sh '+ self.path + ' 2> ~/$file\n'\
            'PID=$!\n'\
            'wait $PID\n'\
            'cd ~\n'\
            'python post_to_spiratest.py '+ self.path +' $file $releaseName\n'    
        
            self.post_to_jenkins_log.append('{} CREATE  Jenkins Job:{}'.format(time.now().strftime("%Y-%m-%d %H:%M:%S"),self.path))
            self.post.create_job(self.path, desc, cmd)
            sleep(1.53)
            #Refresh Jenkins the list of jobs
            self.jobs = self.post.get_jobs_list()
            sleep(1.33)
        
        
        elif self.is_existed_job(self.path) == True:
            
            desc = 'PATH: {}\n'\
                'UPDATE: {}\n'\
                '--------------------\n'\
                .format(self.path,time.now().strftime("%Y-%m-%d %H:%M:%S"))
            
            for file_path in self.json:
                desc += '[' + file_path + ']\n'
                for cls in self.json[file_path]:
                #Add function name in class and its annotation to the description
                    for func in self.json[file_path][cls]['func'].keys():
                        desc += '    ' + cls + '::' +func+'\n'
                        """
                        for tmp in self.json[file_path][cls]['func'][func].get('annotation','').split(','):
                            desc += '        ' + tmp + '\n'
                        desc += '\n'
                        """
                        
            cmd = 'cd /opt/stack/tempest\n'\
            'file=TempestLog/`date +%s`.log\n'\
            './run_tempest.sh '+ self.path + ' 2> ~/$file\n'\
            'PID=$!\n'\
            'wait $PID\n'\
            'cd ~\n'\
            'python post_to_spiratest.py '+ self.path +' $file $releaseName\n'
            
            self.post_to_jenkins_log.append('{} UPDATE  Jenkins Job:{}'.format(time.now().strftime("%Y-%m-%d %H:%M:%S"),self.path))
            self.post.update_job(self.path, desc, cmd)
            sleep(1.53)
            #Refresh Jenkins the list of jobs
            self.jobs = self.post.get_jobs_list()
            sleep(1.33)
        
        else:
            pass
    
    
    def is_existed_job(self,job_name):
        
        for job in self.jobs:
            if job['name'] == job_name:
                return True
        
        return False
    
    def pirnt_log(self):
        
        for log in self.post_to_jenkins_log:
            print log
            
if __name__ == '__main__':
    
    post = PostToJenkins()
    #post.create_one_job('tempest/tempest/api/compute')
    
    #Initial config 
    config = ConfigParser.RawConfigParser(allow_no_value=True)
    config.read('config.cfg')
    path  = config.get('Tempest','api')
    
    """
    if len(sys.argv) < 2:
        print 'no Tempest api path, format =>path/tempest/tempest/api'
        sys.exit()
    else:
        path = sys.argv[1]
    """
    #Create or update Tempest API job
    count = 0
    for dirPath, dirNames, fileNames in os.walk(path):
        if count<1:
            for dirName in dirNames:
                post.create_one_job(path+'/'+dirName)
            count+=1
        else:
            break
    
    #Create or update Tempest Scenario job
    path = config.get('Tempest','scenario')
    post.create_one_job(path)
        
        
    print '--------------------------------'
    post.pirnt_log()
    
    #path = config.get('Tempest','scenario')
    #post.create_one_job(path)

    