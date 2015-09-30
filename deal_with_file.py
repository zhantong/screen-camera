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

if __name__=='__main__':
	path='第七讲.ppt'
	uncompress(com(path),'text1')