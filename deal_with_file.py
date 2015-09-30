from PIL import Image
import re
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

def uncompress(code,path):
	print('-------')
	b = bytearray([int(code[x:x+8], 2) for x in range(0, len(code), 8)])
	with open(path,'wb') as f:
		f.write(b)
def to_image(code):
	img=Image.new('1',(20,20))
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
	img.save('text.bmp')
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
	match=re.search(r'01+$',result)
	return result[:match.start()]
if __name__=='__main__':
	path='text'
	#uncompress(com(path),'text1')
	print(com(path))
	to_image(com(path))
	print(from_image('text.bmp'))