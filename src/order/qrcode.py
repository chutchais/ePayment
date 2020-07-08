from django.http import HttpResponse
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt,csrf_protect

# IB=1
# IC=2
# IO=3
# DN=4

def convert_ref1(invoice):
	if invoice == '' :
		return invoice

	if len(invoice) != 11 :
		return invoice

	if invoice[:2] == 'IB':
		return invoice.replace('IB','1')
	if invoice[:2] == 'IC':
		return invoice.replace('IC','2')
	if invoice[:2] == 'IO':
		return invoice.replace('IO','3')
	if invoice[:2] == 'DN':
		return invoice.replace('DN','4')





def get_merchant_id(ref1,ref2,billerId):
	# Convert Ref1
	ref1 = convert_ref1(ref1)

	# billerId 	= 	'123456789012345'
	data_aid 		= '0016A000000677010112'
	data_billerId 	= '01%02d%s' % (len(billerId),billerId)
	data_ref1	 	= '02%02d%s' % (len(ref1),ref1)
	data_ref2	 	= '03%02d%s' % (len(ref2),ref2)
	data_merge 		= '%s%s%s%s' % (data_aid,data_billerId,data_ref1,data_ref2)
	data_final		= '30%02d%s' % (len(data_merge),data_merge)
	print(data_final)
	return data_final

def getCRC(data):
	# import crcmod
	# crc = crcmod.predefined.mkCrcFun('crc-ccitt-false')
	# crc.update(data.encode())
	# hex(crc(data.encode()))
	import crcmod.predefined
	crc = crcmod.predefined.Crc('crc-ccitt-false')
	crc.update(data.encode())
	return crc.hexdigest()

def qr_image(request,data):
	import pyqrcode
	qr = pyqrcode.create(data)
	qr.png("qr.png", scale=6)

	from PIL import Image, ImageFont, ImageDraw
	im = Image.open("qr.png")
	width, height = im.size
	helvetica = ImageFont.truetype("Helvetica.ttf", size=22)
	d = ImageDraw.Draw(im)
	location = (width/4, height-22)
	d.text(location, data, fill=None, font=helvetica)
	im.save('qr_out.png')
	image_data = open("qr_out.png", "rb").read()
	return HttpResponse(image_data, content_type="image/png")

def billing_qr_image(request):
	# taxId	= 	request.GET['tax']
	ref1		= 	request.GET['ref1']
	if 'ref2' in  request.GET:
		ref2		= 	request.GET['ref2']
	else:
		ref2 = ''


	amount		= 	request.GET['amount']
	terminal 	=  	request.GET['terminal']
	# TO set Ref2 to identify Terminal , A0 = 00 , B1 = 01
	if ref2 == '':
		ref2 = '00' if terminal =='LCMT' else '01'

	# Added by Chutchai on June 02,2020 -- version 1.7
	# To support QRid customization
	if 'qrid' in  request.GET:
		qrid		= 	request.GET['qrid']
	else:
		qrid = ''

#	Arrange QR Data
	payload 		= 	'000201'
	methode 		=	'010212'
	# merchantID		=	'30740016A00000067701011201151234567890123450217ABCD20180316999990310M001002003'
	billerid 		= 	'010553811088480' if terminal == 'LCB1' else '011554701016180'
	merchantID 		= 	get_merchant_id(ref1,ref2,billerid)
	currencyCode 	= 	'5303764' #Fix Value
	amount			=   '54%02d%s' % (len(str(amount)),amount)
	countryCode 	=	'5802TH'

	merchant 		=   'LCB' if terminal == 'LCB1' else 'LCM'
	merchantName	= 	'59%02d%s' % (len(merchant),merchant)
	# additional		=	'62160712%s001002020' % merchant
	# Modify by Chutchai on May 13,2020 -- version 1.6
	# UniqueNo		=	'D%s%s' % (merchant,ref1)

	# Modify by Chutchai on June 02,2020 -- version 1.7
	UniqueNo		=	'D%s%s' % (merchant,ref1 if qrid == '' else qrid)

	QRid			=	'07%02d%s' % (len(UniqueNo),UniqueNo)
	additional		=	'62%02d%s' % (len(QRid),QRid)
	additionalData 	=	'6304'

	# print('Printing Data : %s' % data )
	# print ('CRC : %s' % getCRC(data))

	import pyqrcode
	data = '%s%s%s%s%s%s%s%s%s' % (payload,methode,merchantID,
								currencyCode,amount,countryCode,merchantName,additional,
								additionalData)
	crc_txt = getCRC(data)
	data = '%s%s' % (data,crc_txt) 
	# print('Printing Data : %s' % data )



	
	qr = pyqrcode.create(data)
	qr.png("qr.png", scale=6)

	from PIL import Image, ImageFont, ImageDraw
	im = Image.open("qr.png")
	width, height = im.size
	helvetica = ImageFont.truetype("Helvetica.ttf", size=22)
	d = ImageDraw.Draw(im)
	

	# d.text(location, data, fill=None, font=helvetica)
	data = ref1 if qrid == '' else qrid #terminal
	font = ImageFont.truetype('arial.ttf', size=14)
	ascent, descent = font.getmetrics()
	(font_width, baseline), (offset_x, offset_y) = font.font.getsize(data)
	# print ('QR code width :%s , Text Width :%s' % (width,font_width))

	location = ((width/2)-(font_width/2), height-22)
	d.text(location, ref1 if qrid == '' else qrid, fill=None, font=font)
	# data

	# Put version on Right&Bottom
	version = '1.8'
	font = ImageFont.truetype('arial.ttf', size=12)
	ascent, descent = font.getmetrics()
	(font_width, baseline), (offset_x, offset_y) = font.font.getsize(version)
	location = (width-(font_width), height-18)
	d.text(location, version, fill=None, font=font)


	im.save('qr_out.png')
	image_data = open("qr_out.png", "rb").read()
	return HttpResponse(image_data, content_type="image/png")

def billing_barcode_image(request):
	# LCMT 0115547010161
	# LCB1 0105538110884
	taxId		= 	request.GET['tax']
	ref1		= 	request.GET['ref1']
	ref2		= 	request.GET['ref2']
	terminal 	=  	request.GET['terminal']

	if 'ref2' in  request.GET:
		ref2		= 	request.GET['ref2']
	else:
		ref2 = ''

	# TO set Ref2 to identify Terminal , A0 = 00 , B1 = 01
	if ref2 == '':
		ref2 = '00' if terminal =='LCMT' else '01'
		
	amount	= 	request.GET['amount']
	# suffix 	=	'10' #TMB work, but KBank not working
	# Modify by Chutchai on June 11,2020
	# change from 00 to 10 to support TMB (version 1.8)
	suffix 	=	'10'

	# Convert Ref1
	ref1 = convert_ref1(ref1)

	from barcode.writer import ImageWriter
	import barcode
	EAN = barcode.get_barcode_class('code128')
	# EAN.default_writer_options['write_text'] = False
	# EAN.default_writer_options['human'] = 'ABC'
	# EAN.render(self.writer.ImageWriter,text='sdas')
	
	# data = '|%s\n%s\n%s\n%s\n%s' % (taxId,suffix,ref1,ref2,amount)
	# Modify on March 26, 2020
	# To remove new line and remove Dot on amount

	# data = '|%s%s\r\n%s\r\n%s\r\n%s' % (taxId,suffix,ref1,ref2,amount.replace('.',''))
	# Update on Apr 30,2020 -- Remove New Line
	data = '|%s%s\r%s\r%s\r%s' % (taxId,suffix,ref1,ref2,amount.replace('.',''))
	print(data)
	ean = EAN(data, writer=ImageWriter())
	# ean.render(writer_options=ImageWriter(),text='sds')
	fullname = ean.save('barcode')

	#Add Text below Barcode 
	from PIL import Image, ImageFont, ImageDraw
	im = Image.open("barcode.png")
	width, height = im.size
	d = ImageDraw.Draw(im)
	# print ('Barcode size : %s %s' % (width, height))

	# data = 'LCB1&LCMT'
	# data = data.replace('\n','     ')
	data = '|    %s    %s    %s    %s    %s' % (taxId,suffix,ref1,ref2,amount)
	font = ImageFont.truetype('arial.ttf', size=28)
	ascent, descent = font.getmetrics()
	(font_width, baseline), (offset_x, offset_y) = font.font.getsize(data)
	# print ('Text Width :%s' % (font_width))

	font.width = width
	location = ((width/2)-(font_width/2), height-80)
	d.text(location, data, fill=(0,0,0), font=font)


	# Put version on Right&Bottom
	version = 'Version 1.8'
	font = ImageFont.truetype('arial.ttf', size=12)
	ascent, descent = font.getmetrics()
	(font_width, baseline), (offset_x, offset_y) = font.font.getsize(version)
	location = (width-(font_width), height-60)
	d.text(location, version, fill=(0,0,0), font=font)


	im.save('barcode_out.png')
	
	cropped_example = im.crop((0, 0, width, height-40))
	cropped_example.save('barcode_new.png')
	image_data = open("barcode_new.png", "rb").read()

	return HttpResponse(image_data, content_type="image/png")