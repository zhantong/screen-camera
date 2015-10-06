from PIL import Image
import math
import time
COUNT_WHITE=3
COUNT_LENGTH=100
NUM_BLOCK=50
RATIO=8

def black_white(img,pixels):
	start_time=time.time()
	for row in range(img.size[0]):
		for line in range(img.size[1]):
			if pixels[row,line][0]<100 or pixels[row,line][1]<100 or pixels[row,line][2]<100 :
				pixels[row,line]=(0,0,0)
			else:
				pixels[row,line]=(255,255,255)
	end_time=time.time()
	print('black_white uses %.2f seconds.'%(end_time-start_time))
	#img.save('tt1.jpg')
def rotate(img,pixels):
	start_time=time.time()
	line=img.size[1]//2
	row=1
	while not (pixels[row,line][0]==0 and pixels[row-1,line][0]==255):
		row+=1
	row_orig,line_orig=row,line
	row_lt,line_lt=0,0
	flag=0
#	while 1:
#		flag_1=0
#		line-=1
#		if not pixels[row,line][0]:
#			while not pixels[row,line][0]:
#				row-=1
#			row+=1
#		else:
#			row_final=row
#			count=0
#			t=row
#			while pixels[row,line][0]:
#				count+=1
#				row-=1
#				if count>COUNT_WHITE:
#					count_1=0
#					row=t
#					while pixels[row,line][0]:
#						count_1+=1
#						row+=1
#						print(row,line,pixels[row,line])
#						if count_1>COUNT_WHITE:
#							line_final=line-1
#							flag=1
#							flag_1=1
#							break
#				if flag_1:
#					break
#		if flag:
#			break
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
	#digree=math.atan((row_d-row_final)/(line_d-line_final))*180/math.pi
	#print(row_final,line_final,row_d,line_d,digree)
	#img=img.rotate(-digree)
	#return img
	end_time=time.time()
	print('get the 4 border uses %.2f seconds.'%(end_time-start_time))
	return{
	'lt':{'row':row_lt,'line':line_lt},
	'lb':{'row':row_lb,'line':line_lb},
	'rt':{'row':row_rt,'line':line_rt},
	'rb':{'row':row_rb,'line':line_rb},
	}

def get_border(img,pixels):
	row=0
	result=[]
	img.save('tt2.jpg')
	flag_b=0
	while row<img.size[0]:
		line=1
		count=0
		flag=0
		line_start=0
		while line<img.size[1]:
			if pixels[row,line][0]==0 and pixels[row,line-1][0]==255:
				count=0
				flag=1
				line_start=line
			count+=1
			if pixels[row,line][0]==255 and pixels[row,line-1][0]==0:
				if count>COUNT_LENGTH and flag:
					result.append({
						'row_start':row,
						'line_start':line_start,
						'line_end':line,
						'length':count
						})
					if len(result)>1:
						if 0.9*result[-2]['line_end']>result[-1]['line_end']:
							print(result)
							flag_b=1
							for i in range(len(result)-2,0,-1):
								if 0.9*result[i]['line_end']>result[i-1]['line_end']:
									result=result[i:-1]
									break
							result=result[:-1]
			if flag_b:
				break
			line+=1
		if flag_b:
			break
		row+=1
	line_start=min(item['line_start'] for item in result)
	line_end=max(item['line_end'] for item in result)
	#print(line_start,line_end)
	line=img.size[1]-1
	result=[]
	flag_b=0
	while line>0:
		row=1
		count=0
		flag=0
		row_start=0
		while row<img.size[0]:
			if pixels[row,line][0]==0 and pixels[row-1,line][0]==255:
				count=0
				flag=1
				row_start=row
			count+=1
			if pixels[row,line][0]==255 and pixels[row-1,line][0]==0:
				if count>COUNT_LENGTH and flag:
					result.append({
						'row_start':row_start,
						'row_end':row,
						'line_start':line,
						'length':count
						})
					if len(result)>1:
						if 0.9*result[-2]['row_end']>result[-1]['row_end']:
							print(result)
							flag_b=1
							for i in range(len(result)-2,0,-1):
								if 0.9*result[i]['row_end']>result[i-1]['row_end']:
									result=result[i:-1]
									break
							result=result[:-1]
			if flag_b:
				break
			row+=1
		if flag_b:
			break
		line-=1
	row_start=min(item['row_start'] for item in result)
	row_end=max(item['row_end'] for item in result)
	#print(row_start,row_end)
	return {
	'row_start':row_start,
	'row_end':row_end,
	'line_start':line_start,
	'line_end':line_end
	}

paras={}
def cal_paras(img,pixels):
	img.save('tt1.jpg')
	global paras
	x=RATIO*52
	org=rotate(img,pixels)
	x0=org['lt']['row']
	y0=org['lt']['line']
	x3=org['lb']['row']
	y3=org['lb']['line']
	x2=org['rb']['row']
	y2=org['rb']['line']
	x1=org['rt']['row']
	y1=org['rt']['line']
	print('(x0,y0):(%f,%f)\n(x1,y1):(%f,%f)\n(x2,y2):(%f,%f)\n(x3,y3):(%f,%f)'%(x0,y0,x1,y1,x2,y2,x3,y3))
	print('length:%i'%x)
#	b=(x2-x1)/x
#	d=x1
#	h=y1
#	e=(y4-y1)/x
#	m=((x1-x2+x3-x4)*(y2-y3)+(-y1+y2-y3+y4)*(y4-y3))/(x*((x4-x3)*(y2-y3)-(x2-x3)*(y4-y3)))
#	n=(x1-x2+x3-x4-m*x*(x4-x3))/(x*(y4-y3))
#	a=(x4+m*x*x4+n*x*y4-d)/x
#	f=(y2+m*x*x2+n*x*y2-h)/x
	paras['c']=x0
	paras['b']=(x3-x0)/x
	paras['f']=y0
	paras['d']=(y1-y0)/x
	paras['h']=((x3-x2)*(x0-x1+x2-x3)-(x1-x2)*(y0-y1+y2-y3))/(x*((x3-x2)*(y1-y2)-(x1-x2)*(y3-y2)))
	paras['g']=(x0-x1+x2-x3-x*(y1-y2)*paras['h'])/(x*(x1-x2))
	paras['a']=(x1-x0)/x+x1*paras['g']+y1*paras['h']
	paras['e']=(y3-y0)/x+x3*paras['g']+y3*paras['h']
	print('(x0,y0):(%f,%f)\n(x1,y1):(%f,%f)\n(x2,y2):(%f,%f)\n(x3,y3):(%f,%f)'%(cal_coor(0,0)[0],cal_coor(0,0)[1],cal_coor(RATIO*52,0)[0],cal_coor(RATIO*52,0)[1],cal_coor(RATIO*52,RATIO*52)[0],cal_coor(RATIO*52,RATIO*52)[1],cal_coor(0,RATIO*52)[0],cal_coor(0,RATIO*52)[1]))
	#print(a,b,d,e,f,h,m,n)

def cal_coor(row,line):
	(x,y)=((paras['a']*row+paras['b']*line+paras['c'])/(paras['g']*row+paras['h']*line+1),(paras['d']*row+paras['e']*line+paras['f'])/(paras['g']*row+paras['h']*line+1))
	return (x,y)

def reco(img,pixels):
	b=get_border(img,pixels)
	#line_start=max(item['line_start'] for item in b)
	#line_end=min(item['line_end'] for item in b)
	#lenth=min(item['length'] for item in b)
	#row_start=b[0]['row_start']
	row_start=b['row_start']
	row_end=b['row_end']
	line_start=b['line_start']
	line_end=b['line_end']
	#block_length=(line_end-line_start+1)/(NUM_BLOCK+2)
	block_length=(line_end-line_start+row_end-row_start)/(2*(NUM_BLOCK+2))
	b_length=round(block_length)
	#print(row_start,line_start,line_end,lenth,block_length,b_length)
	print(row_start,line_start,row_end,line_end,block_length,b_length)
	result=''
	mini=b_length*b_length//2
	for line in range(1,NUM_BLOCK+1):
		top=round(line_start+line*block_length)
		for row in range(1,NUM_BLOCK+1):
			left=round(row_start+row*block_length)
			#print(left,top)
			count_w,count_b=0,0
			for i in range(b_length):
				for j in range(b_length):
					if pixels[left+i,top+j][0]:
						count_w+=1
					else:
						count_b+=1
				if count_w>mini:
				#if count_w>mini*1.5:
					result+='1'
					break
				if count_b>=mini:
				#if count_b>mini*0.5:
					result+='0'
					break
			if True:
				if count_w<mini+1 and count_b<mini:
					print(mini,left,top,count_w,count_b)
	return result

def reco_1(pixels):
	result=''
	mid=RATIO*RATIO//2
	for i in range(RATIO,RATIO*51,RATIO):
		for j in range(RATIO,RATIO*51,RATIO):
			x,y=cal_coor(i,j)
			pixels[x,y]=(255,0,0)
			count_w,count_b=0,0
			for a in range(RATIO):
				for b in range(RATIO):
					x,y=cal_coor(j+b,i+a)
					if pixels[x,y][0]:
						count_w+=1
					else:
						count_b+=1
				if count_w>mid:
					result+='1'
					break
				if count_b>mid:
					result+='0'
					break
	return result

global p
p={}
def test():
	global p
	org=rotate(img,pixels)
	p['x0']=org['lt']['row']
	p['y0']=org['lt']['line']
	p['x3']=org['lb']['row']
	p['y3']=org['lb']['line']
	p['x2']=org['rb']['row']
	p['y2']=org['rb']['line']
	p['x1']=org['rt']['row']
	p['y1']=org['rt']['line']
	print(p)

def rec(row,line):
	a0=p['x0']+(p['x1']-p['x0'])*row/52
	b0=p['y0']+(p['y1']-p['y0'])*row/52
	a1=p['x3']+(p['x2']-p['x3'])*row/52
	b1=p['y3']+(p['y2']-p['y3'])*row/52
	x=a0+(a1-a0)*line/52
	y=b0+(b1-b0)*line/52
	return (x,y)


if __name__=='__main__':
	start_time=time.time()
	#img=Image.open('test/007.png')
	img=Image.open('h.jpg')
	#img=img.rotate(-90)
	pixels=img.load()
	black_white(img,pixels)
	#img=rotate(img,pixels)
	#print(rotate(img,pixels))
	#cal_paras(img,pixels)
	#print(cal_coor(5100,5100))
	#res=reco_1(pixels)
	#print(res,len(res))
	#pixels=img.load()
	#res=reco(img,pixels)
	#print(res,len(res))

	test()
	print(rec(0,0),rec(52,0),rec(0,52),rec(52,52))
	for i in range(53):
		for j in range(53):
			#pass
			t=rec(i,j)
			pixels[t[0],t[1]]=(255,0,0)

	img.save('tt2.jpg')
	end_time=time.time()
	print('%.2f'%(end_time-start_time))

