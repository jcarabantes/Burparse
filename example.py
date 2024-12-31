import sys
from burparse import Burparse

b = Burparse(sys.argv[1])

# Access properties
print("[+] Method: " + b.get_method())  # Outputs the HTTP method
print("[+] Headers: " + str(b.get_headers()))  # Outputs all headers
print("[+] Body: " + str(b.get_body()))  # Outputs the body

# Manipulate headers
print("[+] Authorization: " + b.get_header("Authorization"))  # Get specific header
b.set_header("Authorization", "Bearer newtoken")  # Set specific header

# Get URI
# Outputs: /thepath/goes/here
print("[+] URI: " + b.get_uri())
b.set_uri("/newpath/here")
print("[+] URI: " + b.get_uri())


# Get Query String
# Outputs: clientSuppliersList=inactiveSuppliers&pageNo=1&pageSize=10
print("[+] Query string: " + b.get_query_string())
b.set_query_string("newParam=value&anotherParam=123")
print("[+] Query string: " + b.get_query_string())


# Get Query Parameters
# Outputs: {'clientSuppliersList': ['inactiveSuppliers'], 'pageNo': ['1'], 'pageSize': ['10']}
print("[+] Query params: " + str(b.get_query_params()))
b.set_query_params({"param1": "value1", "param2": ["value2", "value3"]})
print("[+] Query params: " + str(b.get_query_params()))
print("[+] Query string: " + b.get_query_string())


print("\n================= FULL REQUEST ==============\n")
print(b)

# Change method or body
# First requests is a GET req, of course...
b.change_method("POST")
b.set_body({"Name": "Red", "Surname": "Smasher"})  # Automatically updates Content-Type to JSON
# print(b)
