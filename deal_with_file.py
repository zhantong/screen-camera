from PIL import Image
import re
import os
img_length=50
def compress(path):
	with open(path,'rb') as f:
		src=f.read()
	result=[]
	for i in src:
		t=bin(i)[2:].zfill(8)
		#t+='0'*(8-len(t))
		result.append(t)
	return ''.join(result)

def com(path):
	with open(path,'rb') as f:
		src=f.read()
	return ''.join(bin(byte)[2:].zfill(8) for byte in src)

def uncom(code,path):
	print('-------')
	b = bytearray([int(code[x:x+8], 2) for x in range(0, len(code), 8)])
	with open(path,'wb') as f:
		f.write(b)
def to_image(code,path):
	img=Image.new('1',(img_length,img_length))
	pixels=img.load()
	length=len(code)
	c=0
	flag=1
	for line in range(img.size[1]):
		for row in range(img.size[0]):
			if c<length:
				pixels[row,line]=int(code[c])
				c+=1
			else:
				pixels[row,line]=1
				if flag:
					pixels[row,line]=0
					flag=0
	img.save(path)
def to_images(code,path):
	count=1
	for item in range(0,len(code),img_length*img_length):
		t=code[item:item+img_length*img_length]
		to_image(t,path+'/'+str(count).zfill(5)+'.bmp')
		count+=1
def from_image(path):
	img=Image.open(path)
	pixels=img.load()
	result=''
	for line in range(img.size[1]):
		for row in range(img.size[0]):
			if pixels[row,line]==0:
				result+='0'
			else:
				result+='1'
	return result
def from_images(path):
	result=''
	for file_name in os.listdir(path):
		print('dealing with %s'%file_name)
		result+=from_image(path+'/'+file_name)
	match=re.search(r'01+$',result)
	return result[:match.start()]
if __name__=='__main__':
	path='file/com073-buiA.docx'
	#uncompress(com(path),'text1')
	#print(com(path))
	#to_image(com(path),'result/text.bmp')
	to_images(com(path),'result/images')
	#uncom(from_image('result/text.bmp'),'result/text')
	uncom(from_images('result/images'),'result/text')