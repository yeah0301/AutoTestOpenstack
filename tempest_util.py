#coding=UTF-8
import os
from macpath import dirname
import re
from sets import Set


def count_test_case_func(path):
	
	test_case_set = Set()

	for root, dirs, files in os.walk(path):
		print root

		for file in files:
			file_path = os.path.join(root, file)
			#print(file_path)
			
			#read every file
			with open(file_path) as f:
				for line in f:
					
					#search the format of function is 'def test_*()' 
					if 'def test_' in line:
						#test_case = re.sub('\s*def test_(\S+)\(\S+\):\s*','def test_\g<1>()',line)
						test_case = line.strip(' \t\n\r')
						#print(test_case)
						if test_case not in test_case_set:
							test_case_set.add(test_case)
						#duplicate restful_spiratest case key
						else:
							print(test_case)
						
						
	print(len(test_case_set))

def parser_test_case_return_json(path):
	"""
		The example of format after parsing Tempest python file  
		
		{
			'tempest\path\python_file' :{
				'class name' :{
					definition:the annotation of class(String)
					func :{
						'function1' :{
							annotation:(String)
						},
						'function2':{
							annotation:(String)
						}
					}
				}
			}
		}
	"""
	
	result = {}

	for root, dirs, files in os.walk(path):
		
		for file in files:
			absolute_file_path = os.path.join(root, file)
			
			#Check whether file name contains substring 'test_'
			if 'test_' in absolute_file_path:
				
				absolute_file_path = absolute_file_path.replace('\\','/')
				
				print(absolute_file_path)
				
				previous_line_is_func = False
				previous_line_is_annotation = False
				
				currentClass = ''
				currentfunc = ''
				
				class_annotation_count = 0;
				
				
				result[absolute_file_path] = {}
				
				for line in open(absolute_file_path):
					line = line.strip(' \t\n\r')
					
					if re.match('class (\\S+)\s*\(\\S*\)', line):
						currentClass = re.sub('class (\\S+)\(\\S*\):', '\g<1>', line)
						result[absolute_file_path][currentClass] = {}
						result[absolute_file_path][currentClass]['func'] = {}
						result[absolute_file_path][currentClass]['definition'] = ''
						count = 0;
					
					elif '"""' in line and class_annotation_count in range(2) :
						result[absolute_file_path][currentClass]['definition'] += line
						class_annotation_count+=1
					
					elif class_annotation_count is 1 :
						result[absolute_file_path][currentClass]['definition'] += line
						
					elif '"""' in line :
						result[absolute_file_path][currentClass]['definition'] = line
						class_annotation_count+=1
					
					elif 'def test_' in line:
						previous_line_is_func = True
						currentfunc = re.sub('def test_(\\S+)\(\\S*\):', 'test_\g<1>()', line)
						print('\t'+currentClass+'::'+currentfunc)
						result[absolute_file_path][currentClass]['func'][currentfunc] = {}
						
					#function annotation
					elif '#' in line and previous_line_is_func:
						previous_line_is_func = False
						previous_line_is_annotation = True
						#print('\t'+line)
						result[absolute_file_path][currentClass]['func'][currentfunc]['annotation'] = line
					
					elif '#' in line and previous_line_is_annotation:
						#print('\t'+line)
						result[absolute_file_path][currentClass]['func'][currentfunc]['annotation'] += ','+line
					
					else:
						previous_line_is_func = False
						previous_line_is_annotation = False
						
			else:
				continue		
									
	return result
	
if __name__ == '__main__':

	print parser_test_case_return_json('tempest\\tempest\\scenario')
	#print parser_test_case_return_json('tempest/tempest/api/compute')
	
	
	
		