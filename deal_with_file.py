from PIL import Image
import re
import os
img_length = 200  # 二维码边长（不包含边界）
width = 4  # 每个方块边长


def com(path):
    """将文件读取为二进制字符串
    """
    with open(path, 'rb') as f:
        src = f.read()
    return ''.join(bin(byte)[2:].zfill(8) for byte in src)


def uncom(code, path):
    """将二进制字符串还原为文件
    """
    b = bytearray([int(code[x:x+8], 2) for x in range(0, len(code), 8)])
    with open(path, 'wb') as f:
        f.write(b)


def to_image(code, path):
    """将二进制字符串转为为二维码
    此时字符串长度事先确定，即不会超出二维码容量
    对于生成的二维码，有白色边界，黑色边界和黑白交替方块
    此时只填充实际作为二进制流的方块，边框随后增加
    """
    img = Image.new(
        '1', (img_length+6*width, img_length+6*width))  # 新建图片，预留每边宽度为3的空间
    pixels = img.load()  # 图片RGB二维矩阵
    length = len(code)
    c = 0
    flag = 1
    for line in range(3*width, img.size[1]-3*width, width):
        for row in range(3*width, img.size[0]-3*width, width):
            if c < length:
                for i in range(width):
                    for j in range(width):
                        pixels[row+i, line+j] = int(code[c])
                c += 1
            else:  # 如果字符串长度小于二维码容量，则填充【01111...】即【黑白白...】
                for i in range(width):
                    for j in range(width):
                        pixels[row+i, line+j] = 1
                if flag:
                    for i in range(width):
                        for j in range(width):
                            pixels[row+i, line+j] = 0
                    flag = 0
    add_frame(pixels, img.size[0])
    img.save(path)


def add_frame(pixels, length):
    """增加二维码边框，为图像识别提供便利
    一层宽度为1（一个方块）的白色边框
    一层宽度为1的黑色边框
    一层宽度为1的黑白交替边框
    """
    for p in range(0, length, width):  # 白色即默认值，只用增加黑色边框
        for i in range(width):
            for j in range(width):
                pixels[p+i, j] = 1
                pixels[p+i, length-1-j] = 1
                pixels[i, p+j] = 1
                pixels[length-1-i, p+j] = 1
    for p in range(0, length-width*2, width*2):  # 增加黑白交替边框
        for i in range(width):
            for j in range(width):
                pixels[2*width+i, p+j] = 1
                pixels[p+i, 2*width+j] = 1
                pixels[length-3*width+i, p+j] = 1
                pixels[p+i, length-3*width+j] = 1


def to_images(code, path):
    """将二进制字符串切片，并分别转换为二维码
    """
    count = 1
    # for循环step为二维码容量
    for item in range(0, len(code), (img_length//width)*(img_length//width)):
        t = code[item:item+(img_length//width)*(img_length//width)]
        to_image(t, path+'/'+str(count).zfill(5)+'.bmp')
        count += 1


def from_image(path):
    """将单个图片转换为二进制字符串
    测试用
    """
    img = Image.open(path)
    pixels = img.load()
    result = ''
    for line in range(3*width, img.size[1]-2*width, width):
        for row in range(3*width, img.size[0]-2*width, width):
            if pixels[row, line] == 0:
                result += '0'
            else:
                result += '1'
    return result


def from_images(path):
    """将路径下所有图片转换为二维码，拼接并消去最后的【01111...】
    测试用
    """
    result = ''
    for file_name in os.listdir(path):
        print('dealing with %s' % file_name)
        result += from_image(path+'/'+file_name)
    match = re.search(r'01*$', result)  # 正则表达式消去最后多余字符
    return result[:match.start()]
if __name__ == '__main__':
    path = 'file/text'
    to_images(com(path), 'result/images')
