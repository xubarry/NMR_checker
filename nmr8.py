#This program check the nmr data
#V5 adds the function of ingore the text before 'H NMR'
#V6 will be able to identify more HiRes type other than ESI and EI
#V8 add the support for GUI


import sys  
import os, re
from tkinter import filedialog
from tkinter import *
import tkinter as tk


def nmr_check(filename = 'nmr.txt'):  	
	filepath = filename

	if not os.path.isfile(filepath):
		print("File path {} does not exist. Exiting...".format(filepath))
		sys.exit()

	with open(filepath) as fp:
		cnt = 1
		results = []
		for line in fp:
			if line.strip() != '':  # ignore the empty lines
				simple_line = re.sub(r'.*H\DNMR', '', line)   #V5 adds the function of ingore the text before 'H NMR' \D means any char other than nmubers
				#print('\n\n')
				#print(simple_line)
				results.append("\nCompound No. " + str(cnt))
				carbon = re.findall('C\d+', simple_line)
				if carbon != []:   #Chenck if Mass is available
					#print(carbon)
					number_carbon = int(re.findall('\d+', carbon[0])[0])

					proton = re.findall('H\d+', simple_line)
					#print(carbon)
					number_proton = int(re.findall('\d+', proton[0])[0])
				
					mass_type = 1
					if len(re.findall('ESI', simple_line)) >= 1:
						if len(re.findall('NH4', simple_line)) >= 1:
							results.append('ESI NH4+')
							mass_type = 4
						elif len(re.findall('\+Na', simple_line)) >= 1:
							results.append('ESI NH4+')
							mass_type = 0
						elif len(re.findall('\+H', simple_line)) >= 1:
							results.append('ESI H+')
							mass_type = 1
					else:
						mass_type = 0 #'EI'
						results.append('EI')
					#print(mass_type)
					number_proton -= mass_type
					#print('Number of carbon from HiRes is: ', number_carbon)

					results.append('Number of proton from HiRes is: '+ str(number_proton))
				else:
					results.append('HiRes is not available')

				space_striped_line = simple_line.strip(' ')  #remove spaces in the data/line
				words = space_striped_line.split(',')
				space_striped_words = [x.strip(' ') for x in words]  #strip the spaces at begining of each word lstrip or strip
				#print(space_striped_words)
				number_of_H = 0
				for word in space_striped_words:
					num = [s for s in re.findall('\d+H\)', word)]
					#print(num)
					number = 0
					if num != []:
						number = int(re.findall('\d+', num[0])[0])
						#print(number)
					number_of_H += number
					#print(number_of_H)
				cnt += 1	
				results.append('Number of proton from addition of NMR is:'+ str(number_of_H))

				if carbon != []:   #Chenck if Mass is available
					if number_of_H == number_proton:
						results.append('Numner of proton is correct.')
					else:
						results.append('Wrong proton number.')
	output_file_name = 'checking_result.txt'
	for each_line in results:
		print(each_line)

	with open(output_file_name, 'w') as file:
		file.writelines(["%s\n" % item  for item in results])


   
root = Tk()
root.filename =  filedialog.askopenfilename(title = "Select file", filetypes = (("NMR txt files","*.txt"),("all files","*.*")))
nmr_check(root.filename)

logo = tk.PhotoImage(file="python_logo_small.gif")

w1 = tk.Label(root, image=logo).pack(side="right")

explanation = """The NMR checking results were saved to file - 'checking_result.txt'"""

w2 = tk.Label(root, 
              justify=tk.LEFT,
              padx = 10, 
              text=explanation).pack(side="left")
root.mainloop()