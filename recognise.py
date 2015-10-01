from PIL import Image
import math

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
	for i in range(1,img.size[0]-1):
		for j in range(1,img.size[1]-1):
			if pixels[i,j][0]==0:
				if pixels[i-1,j][0]==255 and pixels[i,j-1][0]==255 and pixels[i,j+1][0]==255:
					pixels[i,j]=(255,255,255)
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

if __name__=='__main__':
	#black_white()
	#print(rec())
	rotate(rec())