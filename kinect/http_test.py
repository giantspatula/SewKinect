import pickle
import json
import urllib, httplib
import base64

def main():
	with open('point_cloud.p', 'rb') as point_cloud_file:
		point_cloud = point_cloud_file.read()
	with open('body_parts.p', 'rb') as body_parts_file:
		body_parts = body_parts_file.read()
	params = urllib.urlencode({"body_parts": base64.b64encode(body_parts), 
		"point_cloud": base64.b64encode(point_cloud)})
	headers = {"Content-type": "application/x-www-form-urlencoded",
		"Accept": "text/plain"}
	print params
	conn = httplib.HTTPConnection("localhost:5000")
	conn.request('POST', "/calculate", params, headers)
	response = conn.getresponse()
	print response.status, response.reason
	data = response.read()
	conn.close()


if __name__ == '__main__':
	main()