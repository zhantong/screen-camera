"""将拍到的二维码图片转换为原文件
对图片首先进行二值化处理
然后寻找其中二维码的四个顶点
再寻找定位用的黑白交替方块
最后对每个方块进行识别
"""
"""环境
python 3.x
安装pillow库（即原PIL库），windows下可能会有【不能保存为jpg】的问题，linux下没问题
"""
from PIL import Image
import time
import os
import re
COUNT_WHITE = 3  # 寻找四个顶点时的阈值
NUM_BLOCK = 50  # 方块个数（不包含边界和交替方块）


def black_white(img, pixels):
    """二值化处理
    遍历二维矩阵，以RGB阈值将图像变为黑(0,0,0)和白(255,255,255)
    方法比较粗暴
    """
    start_time = time.time()
    for row in range(img.size[0]):
        for line in range(img.size[1]):
            # if pixels[row,line][0]<100 or pixels[row,line][1]<100 or
            # pixels[row,line][2]<100 :
            if pixels[row, line][1] < 150:  # 以G值为阈值
                pixels[row, line] = (0, 0, 0)
            else:
                pixels[row, line] = (255, 255, 255)
    end_time = time.time()
    print('black_white uses %.2f seconds.' % (end_time-start_time))
    # img.save('tt1.jpg')


def find_boarders(img, pixels):
    """找到图像中二维码的四个顶点
    对于左边两个顶点，
    首先从图像中间最左开始向右寻找二维码的黑色边界，
    然后以黑色边界向上（向下）寻找，直到找到顶端，即为顶点
    """
    start_time = time.time()
    line = img.size[1]//2  # 从图像中间开始
    row = 1  # 从图像最左边开始
    # 找到【白黑】特征
    while not (pixels[row, line][0] == 0 and pixels[row-1, line][0] == 255):
        row += 1
    row_orig, line_orig = row, line  # 此时是最初找到的二维码的黑色边界
    row_lt, line_lt = 0, 0  # left top
    flag = 0  # 跳出循环flag

    while 1:
        line -= 1  # 向上寻找
        if pixels[row, line][0]:  # 如果向上为白色
            count = 0
            row_lt = row  # 如果真的到达了顶点，此时row值即为顶点row值
            while pixels[row, line][0]:
                count += 1  # 向右寻找黑色，并计数
                row += 1
                if count > COUNT_WHITE:  # 如果在限定值内未找到黑色，则认为到达上部边界
                    line_lt = line+1  # 前一行即为顶点所在行
                    flag = 1
                    break
            if flag:
                break
        else:
            while not pixels[row, line][0]:  # 如果为黑色则向左寻找到边界【白黑】
                row -= 1
            row += 1
    # print('lt:',row_lt,line_lt)
    """
	接下来寻找另外三个顶点类似，因变量加减值情况不同，所以还是分开写
	"""
    row_lb, line_lb = 0, 0  # left bottom
    flag = 0
    row, line = row_orig, line_orig
    while 1:
        line += 1  # 向下寻找
        if pixels[row, line][0]:
            count = 0
            row_lb = row
            while pixels[row, line][0]:
                count += 1
                row += 1
                if count > COUNT_WHITE:
                    line_lb = line-1  # 前一行即为顶点所在行
                    flag = 1
                    break
            if flag:
                break
        else:
            while not pixels[row, line][0]:
                row -= 1
            row += 1
    # print('lb:',row_lb,line_lb)
    line = img.size[1]//2
    row = img.size[0]-2  # 对于右边两个顶点类似，但从右边边界开始
    while not (pixels[row, line][0] == 0 and pixels[row+1, line][0] == 255):
        row -= 1
    row_orig, line_orig = row, line
    # print(row_orig,line_orig)
    row_rt, line_rt = 0, 0  # right top
    flag = 0
    while 1:
        line -= 1  # 向上寻找
        if pixels[row, line][0]:
            count = 0
            row_rt = row
            while pixels[row, line][0]:
                count += 1  # 若为白色则向左寻找
                row -= 1
                if count > COUNT_WHITE:
                    line_rt = line+1
                    flag = 1
                    break
            if flag:
                break
        else:
            while not pixels[row, line][0]:
                row += 1
            row -= 1
    # print('rt:',row_rt,line_rt)
    row, line = row_orig, line_orig
    row_rb, line_rb = 0, 0  # right bottom
    flag = 0
    while 1:
        line += 1  # 向下寻找
        if pixels[row, line][0]:
            count = 0
            row_rb = row
            while pixels[row, line][0]:
                count += 1
                row -= 1
                if count > COUNT_WHITE:
                    line_rb = line-1
                    flag = 1
                    break
            if flag:
                break
        else:
            while not pixels[row, line][0]:
                row += 1
            row -= 1
    # print('rb:',row_rb,line_rb)
    end_time = time.time()
    print('get the 4 border uses %.2f seconds.' % (end_time-start_time))
    return{
        'lt': {'row': row_lt, 'line': line_lt},
        'lb': {'row': row_lb, 'line': line_lb},
        'rt': {'row': row_rt, 'line': line_rt},
        'rb': {'row': row_rb, 'line': line_rb},
    }


def find_blocks(img, pixels):
    """寻找定位用的黑白交替方块
    找到这些方块的row值或line值，即可计算出图像中任一方块的坐标
    函数最后返回4个长度为50的数组，即为寻找到的50个坐标
    寻找方法即通过之前的四个顶点计算出每个方块的大小，以此将边界点偏移一定值
    沿原边界相同斜率即可找到黑白交替方块，此时即为需要的坐标数据
    为了能够准确对方块定位，尝试了几种不同的方法，只有这种能够达到相当高的精确度
    但对于黑白交替方块的寻找还有很多改进空间
    """
    rowst = []  # rows top
    linesl = []  # lines left
    rowsb = []  # rows bottom
    linesr = []  # lines right
    org = find_boarders(img, pixels)
    p = {
        'x0': org['lt']['row'],
        'y0': org['lt']['line'],
        'x1': org['rt']['row'],
        'y1': org['rt']['line'],
        'x2': org['rb']['row'],
        'y2': org['rb']['line'],
        'x3': org['lb']['row'],
        'y3': org['lb']['line']
    }
    block_length_row = (p['x1']-p['x0'])/(NUM_BLOCK+4)  # 此时并不是方块实际宽度，只是其垂直宽度
    block_length_line = (p['y3']-p['y0'])/(NUM_BLOCK+4)
    off_row = block_length_row*1.25  # 这里的系数1.25对寻找黑白交替方块影响很大，即偏移量
    off_line = block_length_line*1.25
    print('block length row:%.2f, block lenth line:%.2f' %
          (block_length_row, block_length_line))
    print('borders:(x0,y0):(%i,%i)\t(x1,y1):(%i,%i)\t(x2,y2):(%i,%i)\t(x3,y3):(%i,%i)' % (
        p['x0'], p['y0'], p['x1'], p['y1'], p['x2'], p['y2'], p['x3'], p['y3']))
    print('off row:%.2f\toff line:%.2f' % (off_row, off_line))
    """
	下面四个for循环即寻找四组黑白交替方块，相当于是把斜线（边界）平移了一定距离，然后再依次找到黑白交替方块
	"""
    for i in range(p['y0']+round(block_length_line/2), p['y3']):
        if pixels[p['x0']+off_row+(p['x3']-p['x0'])/(p['y3']-p['y0'])*(i-p['y0']), i][0] != pixels[p['x0']+off_row+(p['x3']-p['x0'])/(p['y3']-p['y0'])*(i-1-p['y0']), i-1][0]:
            linesl.append(i)
    if len(linesl) != NUM_BLOCK+2:
        print('count left line blocks wrong:%i' % len(linesl))

    for j in range(p['x0']+round(block_length_row/2), p['x1']):
        if pixels[j, p['y0']+off_line+(p['y1']-p['y0'])/(p['x1']-p['x0'])*(j-p['x0'])][0] != pixels[j-1, p['y0']+off_line+(p['y1']-p['y0'])/(p['x1']-p['x0'])*(j-1-p['x0'])][0]:
            rowst.append(j)
    if len(rowst) != NUM_BLOCK+2:
        print('count top row blocks wrong:%i' % len(rowst))

    for i in range(p['y1']+round(block_length_line/2), p['y2']):
        if pixels[p['x1']-off_row+(p['x2']-p['x1'])/(p['y2']-p['y1'])*(i-p['y1']), i][0] != pixels[p['x1']-off_row+(p['x2']-p['x1'])/(p['y2']-p['y1'])*(i-1-p['y1']), i-1][0]:
            linesr.append(i)
    if len(linesr) != NUM_BLOCK+2:
        print('count right line blocks wrong: counted %i ,detail:' %
              len(linesr), linesr)

    for j in range(p['x3']+round(block_length_row/2), p['x2']):
        if pixels[j, p['y3']-off_line+(p['y2']-p['y3'])/(p['x2']-p['x3'])*(j-p['x3'])][0] != pixels[j-1, p['y3']-off_line+(p['y2']-p['y3'])/(p['x2']-p['x3'])*(j-1-p['x3'])][0]:
            rowsb.append(j)
    if len(rowsb) != NUM_BLOCK+2:
        print('count bottom row blocks wrong:%i' % len(rowsb))
    return {
        'block_length_row': block_length_row,
        'block_length_line': block_length_line,
        'rowst': rowst,
        'linesl': linesl,
        'rowsb': rowsb,
        'linesr': linesr
    }


def reco(img, pixels):
    """对图像中的二维码进行识别
    以每个方块中心的RGB值判断其颜色，即为0还是1
    """
    blocks = find_blocks(img, pixels)
    block_length_row = blocks['block_length_row']
    block_length_line = blocks['block_length_line']
    rowst = blocks['rowst']
    linesl = blocks['linesl']
    rowsb = blocks['rowsb']
    linesr = blocks['linesr']
    result = ''
    for i in range(1, len(linesl)-1):  # 遍历图像中每个方块
        for j in range(1, len(rowst)-1):
            x = rowst[j]+(rowsb[j]-rowst[j])/NUM_BLOCK*i  # 方块的左上角左边
            y = linesl[i]+(linesr[i]-linesl[i])/NUM_BLOCK*j
            # 这样加上半个方块长度后即此方块中心点坐标
            if pixels[x+block_length_row/2, y+block_length_line/2][0]:
                result += '1'
            else:
                result += '0'
            # pixels[x,y]=(0,255,255)#调试用，可以看到寻找到的左上角点在图像中的情况
    # img.save('tt2.jpg')
    return result


def reco_image(path):
    """识别单个图像的全部步骤
    """
    img = Image.open(path)  # 打开图像
    pixels = img.load()  # 加载为RGB的二维矩阵
    black_white(img, pixels)  # 二值化处理
    result = reco(img, pixels)  # 对图像进行识别
    return result


def reco_images(path):
    """识别多个图像
    即遍历路径下的所有图片，汇总得到的结果，并消去最后的无用数据
    """
    result = ''
    last = ''
    for file_name in sorted(os.listdir(path)):
        if file_name.endswith('.png'):
            print('dealing with %s' % file_name)
            res = reco_image(path+'/'+file_name)  # 对单个图片进行处理
            if last:  # 如果此次识别得到的结果和上次相同，则为同一个二维码，舍去
                if res != last:
                    result += res
                    last = res
            else:
                result += res
                last = res
    match = re.search(r'01*$', result)  # 正则表达式消去最后的0111111111
    return result[:match.start()]


def uncom(code, path):
    """转换为文件
    """
    b = bytearray([int(code[x:x+8], 2) for x in range(0, len(code), 8)])
    with open(path, 'wb') as f:
        f.write(b)
if __name__ == '__main__':
    start_time = time.time()
    uncom(reco_images('test'), 'getit')
    end_time = time.time()
    print('used %.2f seconds totally.' % (end_time-start_time))
