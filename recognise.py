from PIL import Image
import math
import re

def black_white():
	img=Image.open('get.jpg')
	#img=img.convert('P')
	pixels=img.load()
	print(img.size[0],img.size[1])
	for i in range(img.size[0]):
		for j in range(img.size[1]):
			if pixels[i,j][0]<200:
				pixels[i,j]=(0,0,0)
			else:
				pixels[i,j]=(255,255,255)
#	for i in range(2,img.size[0]-2):
#		for j in range(2,img.size[1]-2):
#			if pixels[i,j][0]==0:
#				if pixels[i-2,j][0]>200 and pixels[i,j-2][0]>200 and pixels[i+2,j][0]>200:
#					pixels[i,j]=(255,255,255)
	img.save('test1.jpg')

def rec():
	img=Image.open('test1.jpg')
	pixels=img.load()
	line=img.size[1]//2
	row=0
	for i in range(1,img.size[0]):
		if pixels[i,line][0]<50 and pixels[i-1,line][0]>200:
			row=i
			break
	row_orig=row
	line_orig=line
	while 1:
		line-=1
		if pixels[row,line][0]<50:
			while pixels[row,line][0]<50:
				row-=1
			row+=1
		else:
			row_final=row
			count=0
			while pixels[row,line][0]>200:
				count+=1
				row+=1
				if count>3:
					return {
					'from':(row_orig,line_orig),
					'to':(row_final,line-1)
					}

def rotate(data):
	digree=math.atan((data['from'][0]-data['to'][0])/(data['from'][1]-data['to'][1]))*180/3.141592654
	img=Image.open('test1.jpg')
	img=img.rotate(-digree)
	img.save('test2.jpg')

def do():
	img=Image.open('test2.jpg')
	pixels=img.load()
	i=0
	res=[]
	while i<img.size[0]:
		j=1
		count=0
		flag=0
		s=0
		while j<img.size[1]:
			if pixels[i,j][0]<50 and pixels[i,j-1][0]>200:
				count=0
				flag=1
				s=j
			count+=1
			if pixels[i,j][0]>200 and pixels[i,j-1][0]<50:
				if count>100 and flag:
					res.append((i,s,j,count))
					if len(res)>1:
						if 0.9*res[-2][-1]>res[-1][-1]:
							for i in range(len(res)-2,0,-1):
								if 0.9*res[i][-1]>res[i-1][-1]:
									return res[i:-1]
							return res[:-1]
			j+=1
		i+=1

def cal():
	d=do()
	print(d)
	line_start=d[0][1]
	line_end=d[0][2]
	length=d[0][3]
	for item in d:
		if item[1]>line_start:
			line_start=item[1]
		if item[2]<line_end:
			line_end=item[2]
		if item[3]<length:
			length=item[3]
	row_start=d[0][0]
	block_length=(line_end-line_start+1)/52
	b_length=round(block_length)
	print(row_start,line_start,line_end,length,block_length)
	result=''
	m=b_length*b_length//2
	img=Image.open('test2.jpg')
	pixels=img.load()	
	for line in range(1,51):
		top=round(line_start+line*block_length)
		for row in range(1,51):
			left=round(row_start+row*block_length)
			#print(left,top)
			count_w=0
			count_b=0
			for i in range(b_length):
				for j in range(b_length):
					if pixels[left+i,top+j][0]>200:
						count_w+=1
					else:
						count_b+=1
				if count_w>m:
					result+='1'
					break
				if count_b>m:
					result+='0'
					break
	return result
def uncom(code,path):
	match=re.search(r'01*$',code)
	code=code[:match.start()]
	print(code)
	print('-------')
	b = bytearray([int(code[x:x+8], 2) for x in range(0, len(code), 8)])
	with open(path,'wb') as f:
		f.write(b)
if __name__=='__main__':
	#black_white()
	#print(rec())
	#rotate(rec())
	#print(do())
	#cal()
	#print(cal())
	uncom(cal(),'tttt')