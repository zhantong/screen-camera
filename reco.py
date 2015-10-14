from PIL import Image
import time
import os
import re
COUNT_WHITE=3
COUNT_LENGTH=100
NUM_BLOCK=50
RATIO=8

def black_white(img,pixels):
	start_time=time.time()
	for row in range(img.size[0]):
		for line in range(img.size[1]):
			#if pixels[row,line][0]<100 or pixels[row,line][1]<100 or pixels[row,line][2]<100 :
			if pixels[row,line][1]<150:
				pixels[row,line]=(0,0,0)
			else:
				pixels[row,line]=(255,255,255)
	end_time=time.time()
	print('black_white uses %.2f seconds.'%(end_time-start_time))
	#img.save('tt1.jpg')
def find_boarders(img,pixels):
	start_time=time.time()
	line=img.size[1]//2
	row=1
	while not (pixels[row,line][0]==0 and pixels[row-1,line][0]==255):
		row+=1
	row_orig,line_orig=row,line
	row_lt,line_lt=0,0
	flag=0

	while 1:
		line-=1
		if pixels[row,line][0]:
			count=0
			row_lt=row
			while pixels[row,line][0]:
				count+=1
				row+=1
				if count>COUNT_WHITE:
					line_lt=line+1
					flag=1
					break
			if flag:
				break
		else:
			while not pixels[row,line][0]:
				row-=1
			row+=1
	#print('lt:',row_lt,line_lt)
	row_lb,line_lb=0,0
	flag=0
	row,line=row_orig,line_orig
	while 1:
		line+=1
		if pixels[row,line][0]:
			count=0
			row_lb=row
			while pixels[row,line][0]:
				count+=1
				row+=1
				if count>COUNT_WHITE:
					line_lb=line-1
					flag=1
					break
			if flag:
				break
		else:
			while not pixels[row,line][0]:
				row-=1
			row+=1
	#print('lb:',row_lb,line_lb)
	line=img.size[1]//2
	row=img.size[0]-2
	while not (pixels[row,line][0]==0 and pixels[row+1,line][0]==255):
		row-=1
	row_orig,line_orig=row,line
	#print(row_orig,line_orig)
	row_rt,line_rt=0,0
	flag=0
	while 1:
		line-=1
		if pixels[row,line][0]:
			count=0
			row_rt=row
			while pixels[row,line][0]:
				count+=1
				row-=1
				if count>COUNT_WHITE:
					line_rt=line+1
					flag=1
					break
			if flag:
				break
		else:
			while not pixels[row,line][0]:
				row+=1
			row-=1
	#print('rt:',row_rt,line_rt)
	row,line=row_orig,line_orig
	row_rb,line_rb=0,0
	flag=0
	while 1:
		line+=1
		if pixels[row,line][0]:
			count=0
			row_rb=row
			while pixels[row,line][0]:
				count+=1
				row-=1
				if count>COUNT_WHITE:
					line_rb=line-1
					flag=1
					break
			if flag:
				break
		else:
			while not pixels[row,line][0]:
				row+=1
			row-=1
	#print('rb:',row_rb,line_rb)
	end_time=time.time()
	print('get the 4 border uses %.2f seconds.'%(end_time-start_time))
	return{
	'lt':{'row':row_lt,'line':line_lt},
	'lb':{'row':row_lb,'line':line_lb},
	'rt':{'row':row_rt,'line':line_rt},
	'rb':{'row':row_rb,'line':line_rb},
	}



def find_blocks(img,pixels):
	rowst=[]
	linesl=[]
	rowsb=[]
	linesr=[]
	org=find_boarders(img,pixels)
	p={
	'x0':org['lt']['row'],
	'y0':org['lt']['line'],
	'x1':org['rt']['row'],
	'y1':org['rt']['line'],
	'x2':org['rb']['row'],
	'y2':org['rb']['line'],
	'x3':org['lb']['row'],
	'y3':org['lb']['line']
	}
	block_length_row=(p['x1']-p['x0'])/(NUM_BLOCK+4)
	block_length_line=(p['y3']-p['y0'])/(NUM_BLOCK+4)
	off_row=block_length_row*1.25
	off_line=block_length_line*1.25
	print('block length row:%.2f, block lenth line:%.2f'%(block_length_row,block_length_line))
	print('borders:(x0,y0):(%i,%i)\t(x1,y1):(%i,%i)\t(x2,y2):(%i,%i)\t(x3,y3):(%i,%i)'%(p['x0'],p['y0'],p['x1'],p['y1'],p['x2'],p['y2'],p['x3'],p['y3']))
	print('off row:%.2f\toff line:%.2f'%(off_row,off_line))
	for i in range(p['y0']+round(block_length_line/2),p['y3']):
		if pixels[p['x0']+off_row+(p['x3']-p['x0'])/(p['y3']-p['y0'])*(i-p['y0']),i][0]!=pixels[p['x0']+off_row+(p['x3']-p['x0'])/(p['y3']-p['y0'])*(i-1-p['y0']),i-1][0]:
			linesl.append(i)
	if len(linesl)!=NUM_BLOCK+2:
		print('count left line blocks wrong:%i'%len(linesl))

	for j in range(p['x0']+round(block_length_row/2),p['x1']):
		if pixels[j,p['y0']+off_line+(p['y1']-p['y0'])/(p['x1']-p['x0'])*(j-p['x0'])][0]!=pixels[j-1,p['y0']+off_line+(p['y1']-p['y0'])/(p['x1']-p['x0'])*(j-1-p['x0'])][0]:
			rowst.append(j)
	if len(rowst)!=NUM_BLOCK+2:
		print('count top row blocks wrong:%i'%len(rowst))

	for i in range(p['y1']+round(block_length_line/2),p['y2']):
		if pixels[p['x1']-off_row+(p['x2']-p['x1'])/(p['y2']-p['y1'])*(i-p['y1']),i][0]!=pixels[p['x1']-off_row+(p['x2']-p['x1'])/(p['y2']-p['y1'])*(i-1-p['y1']),i-1][0]:
			linesr.append(i)
	if len(linesr)!=NUM_BLOCK+2:
		print('count right line blocks wrong: counted %i ,detail:'%len(linesr),linesr)

	for j in range(p['x3']+round(block_length_row/2),p['x2']):
		if pixels[j,p['y3']-off_line+(p['y2']-p['y3'])/(p['x2']-p['x3'])*(j-p['x3'])][0]!=pixels[j-1,p['y3']-off_line+(p['y2']-p['y3'])/(p['x2']-p['x3'])*(j-1-p['x3'])][0]:
			rowsb.append(j)
	if len(rowsb)!=NUM_BLOCK+2:
		print('count bottom row blocks wrong:%i'%len(rowsb))
	return {
	'block_length_row':block_length_row,
	'block_length_line':block_length_line,
	'rowst':rowst,
	'linesl':linesl,
	'rowsb':rowsb,
	'linesr':linesr
	}


def reco(img,pixels):
	blocks=find_blocks(img,pixels)
	block_length_row=blocks['block_length_row']
	block_length_line=blocks['block_length_line']
	rowst=blocks['rowst']
	linesl=blocks['linesl']
	rowsb=blocks['rowsb']
	linesr=blocks['linesr']
	result=''
	for i in range(1,len(linesl)-1):
		for j in range(1,len(rowst)-1):
			x=rowst[j]+(rowsb[j]-rowst[j])/NUM_BLOCK*i
			y=linesl[i]+(linesr[i]-linesl[i])/NUM_BLOCK*j
			if pixels[x+block_length_row/2,y+block_length_line/2][0]:
				result+='1'
			else:
				result+='0'
			pixels[x,y]=(0,255,255)
	#img.save('tt2.jpg')
	return result

def reco_image(path):
	img=Image.open(path)
	pixels=img.load()
	black_white(img,pixels)
	result=reco(img,pixels)
	return result

def reco_images(path):
	result=''
	last=''
	for file_name in sorted(os.listdir(path)):
		if file_name.endswith('.png'):
			print('dealing with %s'%file_name)
			res=reco_image(path+'/'+file_name)
			if last:
				if res!=last:
					result+=res
					last=res
			else:
				result+=res
				last=res
	match=re.search(r'01*$',result)
	return result[:match.start()]
def uncom(code,path):
	b = bytearray([int(code[x:x+8], 2) for x in range(0, len(code), 8)])
	with open(path,'wb') as f:
		f.write(b)
if __name__=='__main__':
	start_time=time.time()
	uncom(reco_images('test'),'getit')
	end_time=time.time()
	print('used %.2f seconds totally.'%(end_time-start_time))

