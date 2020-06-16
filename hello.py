# """Cloud Foundry test"""
from flask import Flask, render_template, request
import requests, xmltodict, json
import ibm_db
import os
import connect


 
app = Flask(__name__)
 
print(os.getenv("PORT"))
port = int(os.getenv("PORT", 5000))
 
base_url = "http://s3.us-east.cloud-object-storage.appdomain.cloud/adb-sum/"
 
@app.route('/', methods=["GET"])
def get_index_page():
    return render_template('index.html', result={})
    
@app.route('/list_pics', methods=["GET"])
def list_pics():
	# sending get request and saving the response as response object 
	data = requests.get(base_url)
	parse_dict = xmltodict.parse(data.text)
	image_data = parse_dict["ListBucketResult"]["Contents"]
# 	
	return render_template('list_pics.html', result=image_data)
 
#####
# Search by name
#####
@app.route('/search_name', methods=["GET"])
def search_name():
	ret = [];
	return render_template('Search_by_name.html', result=ret)

# search by name function
@app.route('/search_name', methods=["POST"])
def search_by_name():
	name = request.form["name"]

	sql = "SELECT * FROM names WHERE NAME = ?"
	stmt = ibm_db.prepare(connect.connection, sql)

	ibm_db.bind_param(stmt, 1, name)
	result = ibm_db.execute(stmt)

	result_dict = ibm_db.fetch_assoc(stmt)
	
	print(result_dict)
	
	if result_dict is False:
		result_dict = {"NAME":str(name), "RESULT":0}
	else:
		result_dict["RESULT"] = 1
	return render_template('Search_by_name.html', result=result_dict)

#####
# Search by room number
#####

@app.route('/search_room_number', methods=["GET"])
def search_room_number():
	ret = [];
	return render_template('Search_by_room.html', result=ret)

# search by name function
@app.route('/search_room_number', methods=["POST"])
def search_by_romm_number():
	room = str(request.form["room"])
	print(room)
	if room == "":
		print("Here")
		result_dict = {"Room number":str(room), "RESULT":0}
		return render_template('Search_by_room.html', result=result_dict)

	sql = "SELECT * FROM names WHERE ROOM = ?"
	stmt = ibm_db.prepare(connect.connection, sql)

	ibm_db.bind_param(stmt, 1, room)
	result = ibm_db.execute(stmt)

	result_dict = ibm_db.fetch_assoc(stmt)
	print(result_dict)
	
	if result_dict is False:
		result_dict = {"Room number":str(room), "RESULT":0}
# 		print(result_dict)
	else:
		result_dict["RESULT"] = 1
	
	if room is "":
		result_dict = {"Room number":str(room), "RESULT":0}
	return render_template('Search_by_room.html', result=result_dict)

#####
# Update Keyword
#####

@app.route('/update_keyword', methods=["GET"])
def update_keyword():
	ret = [];
	return render_template('Update_Keyword.html', result=ret)
  
# search by name function
@app.route('/update_keyword', methods=["POST"])
def update_keyword_name():
	name = str(request.form["name"])		
	keyword = str(request.form["keyword"])
  
	sql = "UPDATE names SET KEYWORDS = ? WHERE  NAME=?"
	stmt = ibm_db.prepare(connect.connection, sql)
  
	ibm_db.bind_param(stmt, 1, keyword)
	ibm_db.bind_param(stmt, 2, name)
  	
	result = ibm_db.execute(stmt)
  	
	result = ibm_db.num_rows(stmt)
  	
	return render_template('Update_Keyword.html', result=result)
    
####
#Update grade
####
@app.route('/update_points', methods=["GET"])
def update_points():
    ret = [];
    return render_template('update_points.html', result=ret)
  
# search by name function
@app.route('/update_points', methods=["POST"])
def update_update_points():
    name = str(request.form["name"])        
    points = str(request.form["grade"])
    
    if name == "" or points == "":
        result = 0
        return render_template('update_points.html', result=result)
  
    sql = "UPDATE names SET GRADE = ? WHERE  NAME=?"
    stmt = ibm_db.prepare(connect.connection, sql)
  
    ibm_db.bind_param(stmt, 1, points)
    ibm_db.bind_param(stmt, 2, name)
      
    result = ibm_db.execute(stmt)
      
    result = ibm_db.num_rows(stmt)
    
    if name is "" or points is "":
        result = 0
      
    return render_template('update_points.html', result=result)

#######
# With in range
#########
@app.route('/update_range', methods=["GET"])
def update_range():
    ret = [];
    return render_template('Range.html', result=ret)
  
 # search by name functi
@app.route('/update_range', methods=["POST"])
def update_range_name():
    name = str(request.form["first"])        
    keyword = str(request.form["second"])
    
    if name == "" or keyword == "":
        obj = 0
        return render_template('Range.html', result=obj)
    print("ger")
    print(name, keyword)
    sql = " select * from names where GRADE < ? and  GRADE >?"
    stmt = ibm_db.prepare(connect.connection, sql)

    ibm_db.bind_param(stmt, 1, name)
    ibm_db.bind_param(stmt, 2, keyword)
    result = ibm_db.execute(stmt)
    
    ret = []
    result_dict = ibm_db.fetch_assoc(stmt)
    
    while result_dict is not False:
#         print(json.dumps(result_dict))
        ret.append(result_dict)
        result_dict = ibm_db.fetch_assoc(stmt)
        
    data = requests.get(base_url)
    parse_dict = xmltodict.parse(data.text)
    image_data = parse_dict["ListBucketResult"]["Contents"]
    
    img_lt = []
    for data in image_data:
        img_lt.append(data["Key"])
    
    if ret is not False:
        for key in ret:
            if key["PICTURE"] not in img_lt:
                key["PICTURE"] = None
        
    obj = {}
    obj['list'] = ret
 
    
    if name is "" or keyword is "":
        obj = 0
        
#     print(obj)
#     if result_dict is False:
#         result_dict = {"name":str(name), "RESULT":0}
#         print(result_dict)
#     else:
#         result_dict["RESULT"] = 1
#     
#     if name is "" or keyword is "":
#         result_dict = {"name":str(name), "RESULT":0}
    return render_template('Range.html', result=obj)


#######
#Quiz
#DELETE FROM table
# WHERE
#     condition;
#######
# Search details with room
#########
@app.route('/display_room', methods=["GET"])
def display_room():
    ret = [];
    return render_template('display_room.html', result=ret)
  
 # search by name functi
@app.route('/display_room', methods=["POST"])
def display_room_name():
    name = str(request.form["room"])        
    
    if name == "":
        obj = 0
        return render_template('display_room.html', result=obj)
    print("ger")

    sql = " select * from names where ROOM = ?"
    stmt = ibm_db.prepare(connect.connection, sql)

    ibm_db.bind_param(stmt, 1, name)

    result = ibm_db.execute(stmt)
    
    ret = []
    result_dict = ibm_db.fetch_assoc(stmt)
    
    while result_dict is not False:
        ret.append(result_dict)
        result_dict = ibm_db.fetch_assoc(stmt)
        
    data = requests.get(base_url)
    parse_dict = xmltodict.parse(data.text)
    image_data = parse_dict["ListBucketResult"]["Contents"]
    
    img_lt = []
    for data in image_data:
        img_lt.append(data["Key"])
    
    if ret is not False:
        for key in ret:
            if key["PICTURE"] not in img_lt:
                key["PICTURE"] = None
        
    obj = {}
    obj['list'] = ret
 
    
    if name is "":
        obj = 0
        
    return render_template('display_room.html', result=obj)
        
#######
# display_details_point_room
#########
@app.route('/display_details_point_room', methods=["GET"])
def display_details_point_room():
    ret = [];
    return render_template('display_details_point_room.html', result=ret)
  
 # search by name functi
@app.route('/display_details_point_room', methods=["POST"])
def display_details_point_room_name():
    name = str(request.form["first"])        
    keyword = str(request.form["second"])
    room = str(request.form["room"])
    
    if name == "" or keyword == "" or room == "":
        obj = 0
        return render_template('display_details_point_room.html', result=obj)

    sql = " select * from names where GRADE < ? and  GRADE >? and ROOM > ?"
    stmt = ibm_db.prepare(connect.connection, sql)

    ibm_db.bind_param(stmt, 1, name)
    ibm_db.bind_param(stmt, 2, keyword)
    ibm_db.bind_param(stmt, 3, keyword)
    result = ibm_db.execute(stmt)
    
    ret = []
    result_dict = ibm_db.fetch_assoc(stmt)
    
    while result_dict is not False:
        ret.append(result_dict)
        result_dict = ibm_db.fetch_assoc(stmt)
        
    data = requests.get(base_url)
    parse_dict = xmltodict.parse(data.text)
    image_data = parse_dict["ListBucketResult"]["Contents"]
    
    img_lt = []
    for data in image_data:
        img_lt.append(data["Key"])
    
    if ret is not False:
        for key in ret:
            if key["PICTURE"] not in img_lt:
                key["PICTURE"] = None
        
    obj = {}
    obj['list'] = ret
 
    
    if name is "" or keyword is "":
        obj = 0
        

    return render_template('display_details_point_room.html', result=obj)



#######
# modify_name_room_number
#########
@app.route('/modify_name_room_number', methods=["GET"])
def modify_name_room_number():
    ret = [];
    return render_template('modify_name_room_number.html', result=ret)
  
# search by name function
@app.route('/modify_name_room_number', methods=["POST"])
def modify_name_room_number_name():
    name = str(request.form["name"])        
    room = str(request.form["room"])
    
    if name == "" or room == "":
        result= 0
        return render_template('modify_name_room_number.html', result=result)
  
    sql = "UPDATE names SET NAME = ? WHERE  ROOM=?"
    stmt = ibm_db.prepare(connect.connection, sql)
  
    ibm_db.bind_param(stmt, 1, name)
    ibm_db.bind_param(stmt, 2, room)
      
    result = ibm_db.execute(stmt)
      
    result = ibm_db.num_rows(stmt)
      
    return render_template('modify_name_room_number.html', result=result)


####
##Quizreal
####

@app.route('/list_pics_img', methods=["GET"])
def list_pics_img():
    # sending get request and saving the response as response object 
    data = requests.get(base_url)
    parse_dict = xmltodict.parse(data.text)
    image_data = parse_dict["ListBucketResult"]["Contents"]
#     
    return render_template('list_pics_img.html', result=image_data)



#######
# With in range
#########
@app.route('/add', methods=["GET"])
def add():
    ret = [];
    return render_template('add.html', result=ret)
  
 # search by name functi
@app.route('/add', methods=["POST"])
def add_name():
    name = (request.form["first"])        
    keyword = (request.form["second"])
    
    if name == "" or keyword == "":
        obj = "not valid"
        return render_template('add.html', result=obj)
    
    obj = int(name) + int(keyword)
   
    return render_template('add.html', result=obj)




@app.route('/display_details_state', methods=["GET"])
def display_details_state():
    ret = [];
    return render_template('display_details_state.html', result=ret)
  
 # search by name functi
@app.route('/display_details_state', methods=["POST"])
def display_details_state_name():
    name = str(request.form["first"])        
    
    if name == "" :
        obj = 0
        return render_template('display_details_state.html', result=obj)

    sql = " select * from name where STATE= ?"
    stmt = ibm_db.prepare(connect.connection, sql)

    ibm_db.bind_param(stmt, 1, name)

    result = ibm_db.execute(stmt)
    
    ret = []
    result_dict = ibm_db.fetch_assoc(stmt)
    
    while result_dict is not False:
        ret.append(result_dict)
        result_dict = ibm_db.fetch_assoc(stmt)
        
    data = requests.get(base_url)
    parse_dict = xmltodict.parse(data.text)
    image_data = parse_dict["ListBucketResult"]["Contents"]
    
    img_lt = []
    for data in image_data:
        img_lt.append(data["Key"])
    
    if ret is not False:
        for key in ret:
            if key["PICTURE"] not in img_lt:
                key["PICTURE"] = None
        
    obj = {}
    obj['list'] = ret
 
    
    if name is "":
        obj = 0
        

    return render_template('display_details_state.html', result=obj)




@app.route('/update_details_given_name', methods=["GET"])
def update_details_given_name():
    ret = [];
    return render_template('update_details_given_name.html', result=ret)
  
# search by name function
@app.route('/update_details_given_name', methods=["POST"])
def update_details_given_name_name():
    name = str(request.form["name"])        
    state = str(request.form["state"])
    caption = str(request.form["caption"])
    
    if name == "" or state == "" or caption == "":
        result = 0
        return render_template('update_details_given_name.html', result=result)
        
  
    sql = "UPDATE name SET STATE = ?, CAPTION = ? WHERE  NAME=?"
    stmt = ibm_db.prepare(connect.connection, sql)
  
    ibm_db.bind_param(stmt, 1, state)
    ibm_db.bind_param(stmt, 2, caption)
    ibm_db.bind_param(stmt, 3, name)
      
    result = ibm_db.execute(stmt)
      
    result = ibm_db.num_rows(stmt)
    
    print(result)
      
    return render_template('update_details_given_name.html', result=result)






@app.route('/search_pic_name', methods=["GET"])
def search_pic_name():
    ret = [];
    return render_template('search_pic_name.html', result=ret)

# search by name function
@app.route('/search_pic_name', methods=["POST"])
def search_pic_name_name():
    name = request.form["name"]

    sql = "SELECT * FROM names WHERE PICTURE = ?"
    stmt = ibm_db.prepare(connect.connection, sql)

    ibm_db.bind_param(stmt, 1, name)
    result = ibm_db.execute(stmt)

    result_dict = ibm_db.fetch_assoc(stmt)
    
    print(result_dict)
    
    if result_dict is False:
        result_dict = {"PICTURE":str(name), "RESULT":0}
    else:
        result_dict["RESULT"] = 1
    return render_template('search_pic_name.html', result=result_dict)


@app.route('/search_by_id', methods=["GET"])
def search_by_id():
    ret = [];
    return render_template('search_by_id.html', result=ret)
# search by name function
@app.route('/search_by_id', methods=["POST"])
def search_by_id_pic():
    room = str(request.form["room"])
    print(room)
    if room == "":
        print("Here")
        result_dict = {"Room number":str(room), "RESULT":0}
        return render_template('search_by_id.html', result=result_dict)

    sql = "SELECT * FROM names WHERE ROOM = ?"
    stmt = ibm_db.prepare(connect.connection, sql)

    ibm_db.bind_param(stmt, 1, room)
    result = ibm_db.execute(stmt)

    result_dict = ibm_db.fetch_assoc(stmt)
    print(result_dict)
    
    if result_dict is False:
        result_dict = {"Room number":str(room), "RESULT":0}
#         print(result_dict)
    else:
        result_dict["RESULT"] = 1
    
    if room is "":
        result_dict = {"Room number":str(room), "RESULT":0}
    return render_template('search_by_id.html', result=result_dict)


#####
# update_caption
#####

@app.route('/update_caption', methods=["GET"])
def update_caption():
    ret = [];
    return render_template('update_caption.html', result=ret)
  
# search by name function
@app.route('/update_caption', methods=["POST"])
def update_caption_name():
    name = str(request.form["name"])        
    keyword = str(request.form["keyword"])
    
    if name == "" or keyword == "":
        result_dict = {}
        result_dict["RESULT"]=0
        return render_template('update_caption.html', result=result_dict)
        
  
    sql = "UPDATE names SET KEYWORDS = ? WHERE  NAME=?"
    stmt = ibm_db.prepare(connect.connection, sql)
  
    ibm_db.bind_param(stmt, 1, keyword)
    ibm_db.bind_param(stmt, 2, name)
      
    result = ibm_db.execute(stmt)
      
    result = ibm_db.num_rows(stmt)
    
    sql = "SELECT * FROM names WHERE NAME = ?"
    stmt = ibm_db.prepare(connect.connection, sql)

    ibm_db.bind_param(stmt, 1, name)
    result = ibm_db.execute(stmt)

    result_dict = ibm_db.fetch_assoc(stmt)
    print(result_dict)
    
    result_dict["RESULT"] = result
      
    return render_template('update_caption.html', result=result_dict)



#####
#Upload
#####
# import ibm_boto3
# from ibm_botocore.client import Config

# # cos = ibm_boto3.client(service_name='s3',
# #                        ibm_api_key_id='FfdcjIW2tyLy8IiTsLr6unMck63Mwl72uohW28c4Bvyt',
# #                        ibm_service_instance_id='crn:v1:bluemix:public:iam-identity::a/9df81bd7933a4073b416a9631c9e6a5e::serviceid:ServiceId-69e78c34-a758-46d5-bd11-4b0416d8c2d6',
# #                        config=Config(signature_version='oauth'),
# #                        endpoint_url='https://control.cloud-object-storage.cloud.ibm.com/v2/endpoints')
# # 
# # try:
# #     res = cos.upload_file('C:/Users/saipr/Documents/GitHub/Cloud_Summer_2020/hello.jpg',
# #                       'adb-sum', 'l')
# # except Exception as e:
# #     print(Exception, e)
# # else:
# #     print('File Uploaded')
#  
#  
# cos_credentials={
#   "apikey": "FfdcjIW2tyLy8IiTsLr6unMck63Mwl72uohW28c4Bvyt",
#   "iam_serviceid_crn": "crn:v1:bluemix:public:iam-identity::a/9df81bd7933a4073b416a9631c9e6a5e::serviceid:ServiceId-69e78c34-a758-46d5-bd11-4b0416d8c2d6",
#   "resource_instance_id": "crn:v1:bluemix:public:cloud-object-storage:global:a/9df81bd7933a4073b416a9631c9e6a5e:6b6651f3-aeac-4808-9d90-a5017167921f::",
#   'BUCKET': 'adb-sum'
# }
# auth_endpoint = 'https://iam.bluemix.net/oidc/token'
# service_endpoint = 'https://s3-api.us-geo.objectstorage.softlayer.net'
# 
# # auth_endpoint = 'https://iam.bluemix.net/oidc/token'
# # service_endpoint = 'http://s3.us-south.cloud-object-storage.appdomain.cloud'
# cos = ibm_boto3.client('s3',
#                          ibm_api_key_id=cos_credentials['apikey'],
#                          ibm_service_instance_id=cos_credentials['resource_instance_id'],
#                          ibm_auth_endpoint=auth_endpoint,
#                          config=Config(signature_version='oauth'),
#                          endpoint_url=service_endpoint)
# 
# print(cos)
#  
# for bucket in cos.list_buckets()['Buckets']:
#         print(bucket['Name'])
#  
def upload_file_cos(credentials,local_file_name,key, auth_endpoint):  
    cos = ibm_boto3.client('s3',
                         ibm_api_key_id=cos_credentials['apikey'],
                         ibm_service_instance_id=cos_credentials['resource_instance_id'],
                         ibm_auth_endpoint=auth_endpoint,
                         config=Config(signature_version='oauth'),
                         endpoint_url=service_endpoint)
    
    print(cos.list_buckets()['Buckets'][0]['Name'])

    try:
        res=cos.upload_file(Filename=local_file_name, Bucket=cos.list_buckets()['Buckets'][0]['Name'],Key=key)
    except Exception as e:
        print(Exception, e)
    else:
        print('File Uploaded')
        

         
# upload_file_cos(cos_credentials, 'C:/Users/saipr/Documents/GitHub/Cloud_Summer_2020/hello.jpg',
# 			"hello.jpg", auth_endpoint)

# for bucket in cos.list_buckets()['Buckets']:
#     print(bucket['Name'])
#     
# try:
# #     res = cos.upload_file('C:/Users/saipr/Documents/GitHub/Cloud_Summer_2020/hello.jpg',
# #                      cos.list_buckets()['Buckets'][0], 'l')
#     res = cos.upload_file(Filename='hello.jpg',Bucket=cos_credentials['BUCKET'],Key='img.jpg')
# except Exception as e:
#     print(Exception, e)
# else:
#     print('File Uploaded')

# COS_API_KEY_ID = 'FfdcjIW2tyLy8IiTsLr6unMck63Mwl72uohW28c4Bvyt'
# COS_SERVICE_CRN = "crn:v1:bluemix:public:iam-identity::a/9df81bd7933a4073b416a9631c9e6a5e::serviceid:ServiceId-69e78c34-a758-46d5-bd11-4b0416d8c2d6"
# COS_AUTH_ENDPOINT = 'https://iam.cloud.ibm.com/identity/token'
# COS_ENDPOINT = 'http://s3.dal.us.cloud-object-storage.appdomain.cloud'
# def multi_part_upload_manual(bucket_name, item_name, file_path):
#     try:
#         # create client object
#         cos_cli = ibm_boto3.client("s3",
#             ibm_api_key_id=COS_API_KEY_ID,
#             ibm_service_instance_id=COS_SERVICE_CRN,
#             ibm_auth_endpoint=COS_AUTH_ENDPOINT,
#             config=Config(signature_version="oauth"),
#             endpoint_url=COS_ENDPOINT
#         )
# 
#         print("Starting multi-part upload for {0} to bucket: {1}\n".format(item_name, bucket_name))
# 
#         # initiate the multi-part upload
#         mp = cos_cli.create_multipart_upload(
#             Bucket=bucket_name,
#             Key=item_name
#         )
# 
#         upload_id = mp["UploadId"]
# 
#         # min 20MB part size
#         part_size = 1024 * 1024 * 20
#         file_size = os.stat(file_path).st_size
#         part_count = int(math.ceil(file_size / float(part_size)))
#         data_packs = []
#         position = 0
#         part_num = 0
# 
#         # begin uploading the parts
#         with open(file_path, "rb") as file:
#             for i in range(part_count):
#                 part_num = i + 1
#                 part_size = min(part_size, (file_size - position))
# 
#                 print("Uploading to {0} (part {1} of {2})".format(item_name, part_num, part_count))
# 
#                 file_data = file.read(part_size)
# 
#                 mp_part = cos_cli.upload_part(
#                     Bucket=bucket_name,
#                     Key=item_name,
#                     PartNumber=part_num,
#                     Body=file_data,
#                     ContentLength=part_size,
#                     UploadId=upload_id
#                 )
# 
#                 data_packs.append({
#                     "ETag":mp_part["ETag"],
#                     "PartNumber":part_num
#                 })
# 
#                 position += part_size
# 
#         # complete upload
#         cos_cli.complete_multipart_upload(
#             Bucket=bucket_name,
#             Key=item_name,
#             UploadId=upload_id,
#             MultipartUpload={
#                 "Parts": data_packs
#             }
#         )
#         print("Upload for {0} Complete!\n".format(item_name))
#     except ClientError as be:
#         # abort the upload
#         cos_cli.abort_multipart_upload(
#             Bucket=bucket_name,
#             Key=item_name,
#             UploadId=upload_id
#         )
#         print("Multi-part upload aborted for {0}\n".format(item_name))
#         print("CLIENT ERROR: {0}\n".format(be))
#     except Exception as e:
#         print("Unable to complete multi-part upload: {0}".format(e))
#         
        
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)


