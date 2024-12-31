from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import json

class Burparse:
    """
    A utility class to parse, manipulate, and reconstruct raw HTTP requests from a file.
    Author: @jcarabantes
    Attributes:
        filename (str): The file containing the raw HTTP request.
        method (str): The HTTP method (e.g., GET, POST).
        path (str): The full path including URI and query string.
        http_version (str): The HTTP version (e.g., HTTP/1.1).
        headers (dict): A dictionary of HTTP headers.
        body (str): The HTTP request body (if present).
    """

    def __init__(self, filename):
        """
        Initializes the Burparse object by reading and parsing the raw HTTP request from a file.

        Args:
            filename (str): The file containing the raw HTTP request.
        """
        self.filename = filename
        self.method = None
        self.path = None
        self.http_version = None
        self.headers = {}
        self.body = None
        self._parse_raw_file()

    def _parse_raw_file(self):
        """
        Parses the raw HTTP request file into its components: method, path, headers, and body.
        """
        with open(self.filename, 'r') as file:
            lines = file.readlines()

        # Parse request line
        request_line = lines[0].strip()
        self.method, self.path, self.http_version = request_line.split()

        # Parse headers and body
        body_started = False
        for line in lines[1:]:
            line = line.strip()
            if line == '':
                body_started = True
                continue

            if not body_started:
                key, value = line.split(':', 1)
                self.headers[key.strip()] = value.strip()
            else:
                self.body = (self.body or '') + line

    def get_method(self):
        """
        Retrieves the HTTP method.

        Returns:
            str: The HTTP method (e.g., GET, POST).
        """
        return self.method

    def get_headers(self):
        """
        Retrieves all HTTP headers.

        Returns:
            dict: A dictionary of HTTP headers.
        """
        return self.headers

    def get_body(self):
        """
        Retrieves the HTTP request body.

        Returns:
            str: The request body, or None if not present.
        """
        return self.body

    def get_header(self, key):
        """
        Retrieves a specific HTTP header.

        Args:
            key (str): The header name.

        Returns:
            str: The header value, or None if the header does not exist.
        """
        return self.headers.get(key)

    def set_header(self, key, value):
        """
        Sets or updates an HTTP header.

        Args:
            key (str): The header name.
            value (str): The header value.
        """
        self.headers[key] = value

    def change_method(self, new_method):
        """
        Changes the HTTP method.

        Args:
            new_method (str): The new HTTP method (e.g., GET, POST).
        """
        self.method = new_method

    def set_body(self, body):
        """
        Sets the HTTP request body and updates Content-Type if appropriate.

        Args:
            body (str | dict): The new request body. If a dictionary is provided,
            it is automatically converted to JSON.
        """
        self.body = body
        if isinstance(body, dict):
            self.headers["Content-Type"] = "application/json"
            self.body = json.dumps(body)
        elif "=" in body:
            self.headers["Content-Type"] = "application/x-www-form-urlencoded"

    def get_uri(self):
        """
        Extracts the URI from the path.

        Returns:
            str: The URI (path without query string).
        """
        return urlparse(self.path).path

    def set_uri(self, new_uri):
        """
        Sets a new URI and preserves the query string.

        Args:
            new_uri (str): The new URI.
        """
        parsed = urlparse(self.path)
        self.path = urlunparse(parsed._replace(path=new_uri))

    def get_query_string(self):
        """
        Extracts the query string from the path.

        Returns:
            str: The query string.
        """
        return urlparse(self.path).query

    def set_query_string(self, new_query_string):
        """
        Sets a new query string and preserves the URI.

        Args:
            new_query_string (str): The new query string.
        """
        parsed = urlparse(self.path)
        self.path = urlunparse(parsed._replace(query=new_query_string))

    def set_query_params(self, new_params):
        """
        Sets query parameters using a dictionary.

        Args:
            new_params (dict): A dictionary of query parameters.
        """
        new_query_string = urlencode(new_params, doseq=True)
        self.set_query_string(new_query_string)

    def get_query_params(self):
        """
        Parses the query string into a dictionary of parameters.

        Returns:
            dict: A dictionary of query parameters.
        """
        query = self.get_query_string()
        return parse_qs(query)

    def __str__(self):
        """
        Reconstructs the HTTP request as a string.

        Returns:
            str: The reconstructed HTTP request.
        """
        request_line = f"{self.method} {self.path} {self.http_version}"
        headers = "\n".join(f"{k}: {v}" for k, v in self.headers.items())
        return f"{request_line}\n{headers}\n\n{self.body or ''}"
